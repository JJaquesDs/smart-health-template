from pathlib import Path
from uuid import uuid4

from celery.result import AsyncResult
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.celery_client import celery_app
from app.domains.exames.imagem.models import (
    ExameImagem,
    ResultadoExameImagemIa,
    UploadExameImagem,
)

UPLOAD_DIR = Path("uploads")
MAX_IMAGE_BYTES = 10 * 1024 * 1024


def create_exam_with_upload(
    session: Session,
    file: UploadFile,
    tipo: str,
    descricao: str | None = None,
    usuario_id: int | None = None,
    paciente_id: int | None = None,
):
    data = file.file.read(MAX_IMAGE_BYTES + 1)
    if not data or len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, "Envie uma imagem de até 10 MB")
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        extension = ".png"
    elif data.startswith(b"\xff\xd8\xff"):
        extension = ".jpg"
    else:
        raise HTTPException(415, "Formato inválido. Envie JPEG ou PNG")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = uuid4().hex + extension
    path = UPLOAD_DIR / filename
    path.write_bytes(data)
    try:
        exame = ExameImagem(
            tipo=tipo,
            descricao=descricao,
            usuario_id=usuario_id,
            paciente_id=paciente_id,
            link_imagem=f"/exame_imagem/uploads/{filename}",
        )
        session.add(exame)
        session.flush()
        upload = UploadExameImagem(
            titulo=Path(file.filename or filename).name[:255],
            caminho_upload=str(path),
            exame_imagem_id=exame.exame_id,
        )
        session.add(upload)
        session.flush()
        return exame, upload
    except Exception:
        path.unlink(missing_ok=True)
        raise


def serialize_result(result):
    return {
        "status": "SUCCESS",
        "resultado_id": result.resultado_id,
        "exame_imagem_id": result.exame_imagem_id,
        "paciente_id": result.exame_imagem.paciente_id,
        "paciente_nome": result.exame_imagem.paciente.nome
        if result.exame_imagem.paciente
        else None,
        "classe_predita": result.classe_predita,
        "confianca": result.confianca,
        "probabilidades": result.probabilidades,
        "interpretacao": result.interpretacao,
        "data_analise": result.data_analise,
    }


def save_result_analise_service(
    task_id: str, session: Session, interpretacao: str | None = None
):
    # O bloqueio evita inserções duplicadas quando dois polls terminam juntos.
    exame = (
        session.query(ExameImagem).filter_by(task_id=task_id).with_for_update().first()
    )
    if not exame:
        raise HTTPException(404, "Tarefa não encontrada")
    existing = (
        session.query(ResultadoExameImagemIa)
        .filter_by(exame_imagem_id=exame.exame_id)
        .first()
    )
    if existing:
        return serialize_result(existing)
    task = AsyncResult(task_id, app=celery_app)
    try:
        state = task.state
        if state in {"PENDING", "STARTED", "RETRY", "RECEIVED"}:
            return {"status": state}
        if state in {"FAILURE", "REVOKED"}:
            return {
                "status": "FAILURE",
                "detail": "Não foi possível processar a imagem. Confira o formato e tente novamente.",
            }
        if state != "SUCCESS":
            return {"status": "PENDING"}
        data = task.result
    except Exception:
        raise HTTPException(
            503, "Serviço de análise indisponível. Verifique Redis e worker."
        )
    if data.get("exame_img_id") != exame.exame_id:
        raise HTTPException(502, "O resultado não corresponde ao exame solicitado")
    result = ResultadoExameImagemIa(
        classe_predita=data["classe"],
        confianca=data["confianca"],
        probabilidades=data.get("probabilidades") or data["lista"],
        interpretacao=interpretacao,
        exame_imagem_id=exame.exame_id,
    )
    session.add(result)
    session.commit()
    session.refresh(result)
    return serialize_result(result)
