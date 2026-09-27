from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import exigir_role, get_session
from app.core.celery_client import celery_app
from app.domains.exames.imagem.models import (
    ExameImagem,
    UploadExameImagem,
)
from app.domains.exames.imagem.schemas import ExameImagemPublic
from app.domains.exames.imagem.service import (
    UPLOAD_DIR,
    create_exam_with_upload,
    save_result_analise_service,
    serialize_result,
)
from app.domains.pacientes.models import Paciente
from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario

router = APIRouter(prefix="/exame_imagem", tags=["Exames_Imagem"])
access = exigir_role([UserRole.SUPERUSER, UserRole.MEDICO])


def authorize(exame, user):
    if not exame:
        raise HTTPException(404, "Exame não encontrado")
    if user.role != UserRole.SUPERUSER and exame.usuario_id != user.usuario_id:
        raise HTTPException(403, "Sem permissão para acessar este exame")


@router.post("/", response_model=ExameImagemPublic)
def create_image_exam(
    file: UploadFile = File(...),
    tipo: str = Form("citologia"),
    descricao: str | None = Form(None),
    paciente_id: int = Form(...),
    session: Session = Depends(get_session),
    user_atual: Usuario = Depends(access),
):
    if tipo != "citologia":
        raise HTTPException(422, "Este modelo aceita exames de citologia")
    if descricao and len(descricao) > 2000:
        raise HTTPException(422, "Descrição deve ter no máximo 2000 caracteres")
    if not session.get(Paciente, paciente_id):
        raise HTTPException(404, "Paciente não encontrado")
    exame, upload = create_exam_with_upload(
        session, file, tipo, descricao, user_atual.usuario_id, paciente_id
    )
    try:
        session.commit()
    except Exception:
        session.rollback()
        Path(upload.caminho_upload).unlink(missing_ok=True)
        raise
    return exame


@router.get("/")
def history(
    paciente_id: int | None = None,
    session: Session = Depends(get_session),
    user: Usuario = Depends(access),
):
    query = session.query(ExameImagem)
    if user.role != UserRole.SUPERUSER:
        query = query.filter(ExameImagem.usuario_id == user.usuario_id)
    if paciente_id is not None:
        query = query.filter(ExameImagem.paciente_id == paciente_id)
    return [
        {
            "exame_id": e.exame_id,
            "tipo": e.tipo,
            "descricao": e.descricao,
            "task_id": e.task_id,
            "paciente_id": e.paciente_id,
            "paciente_nome": e.paciente.nome if e.paciente else None,
            "arquivo": e.upload_imagem[0].titulo if e.upload_imagem else "",
            "resultado": serialize_result(e.resultados[0]) if e.resultados else None,
        }
        for e in query.order_by(ExameImagem.exame_id.desc()).limit(30)
    ]


@router.get("/uploads/{file_name}")
def get_uploads(
    file_name: str,
    session: Session = Depends(get_session),
    user: Usuario = Depends(access),
):
    path = UPLOAD_DIR / file_name
    if path.resolve().parent != UPLOAD_DIR.resolve():
        raise HTTPException(404, "Arquivo não encontrado")
    upload = (
        session.query(UploadExameImagem).filter_by(caminho_upload=str(path)).first()
    )
    authorize(upload.exames_imagem if upload else None, user)
    if not path.is_file():
        raise HTTPException(404, "Arquivo não encontrado")
    return FileResponse(path)


@router.post("/{exame_id}/analisar")
def analisar_exame(
    exame_id: int,
    reiniciar: bool = False,
    session: Session = Depends(get_session),
    user: Usuario = Depends(access),
):
    exame = (
        session.query(ExameImagem)
        .filter_by(exame_id=exame_id)
        .with_for_update()
        .first()
    )
    authorize(exame, user)
    if not exame.upload_imagem:
        raise HTTPException(422, "Exame não possui imagem")
    if exame.task_id and (not reiniciar or exame.resultados):
        return {"msg": "Análise já solicitada", "task_id": exame.task_id}
    task_id = str(uuid4())
    try:
        celery_app.send_task(
            "process_image",
            args=[exame.upload_imagem[0].caminho_upload, exame_id],
            task_id=task_id,
            retry=False,
        )
    except Exception:
        raise HTTPException(
            503, "Não foi possível iniciar a análise. Verifique Redis e worker."
        )
    exame.task_id = task_id
    session.commit()
    return {"msg": "Análise iniciada", "task_id": task_id}


@router.get("/resultado/{task_id}")
def pegar_resultado_analise(
    task_id: str,
    session: Session = Depends(get_session),
    user: Usuario = Depends(access),
):
    exame = session.query(ExameImagem).filter_by(task_id=task_id).first()
    authorize(exame, user)
    return save_result_analise_service(task_id, session)
