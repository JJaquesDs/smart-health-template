import os

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.deps import exigir_role, get_session

from app.core.celery_client import celery_app

from app.domains.exames.imagem.schemas import (
    ExameImagemCreate,
    ExameImagemPublic,
    UploadExameImagemCreate,
    UploadExameImagemPublic,
    ExameComUploadResponse
)

from app.domains.exames.imagem.service import (
    create_exam_with_upload,
    save_result_analise_service
)

from app.domains.exames.imagem.repository import get_exame_image

from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario


router = APIRouter(prefix="/exame_imagem", tags=["Exames_Imagem"])


@router.post(
    path="/",
    response_model=ExameImagemPublic,
    summary="Criar um Exame de imagem com Upload"
)
def create_image_exam(
        file: UploadFile = File(...),
        tipo: str = Form("citologia"),
        descricao: str | None = Form(None),
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role([UserRole.SUPERUSER, UserRole.MEDICO]))
):
    """ Rota para salvar um exame de imagem"""

    try:
        exame, upload = create_exam_with_upload(session=session, file=file, tipo=tipo, descricao=descricao)

        session.commit()

        return exame

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar exame")


@router.get("/uploads/{file_name}")
def get_uploads(
        file_name: str,
        user: Usuario = Depends(exigir_role(roles=[
            UserRole.SUPERUSER, UserRole.ADMIN, UserRole.MEDICO])
        ),
        session: Session = Depends(get_session)
):
    """ Rota para vizualizar os exames de imagem """

    caminho = os.path.join("uploads", file_name)

    if not os.path.exists(caminho):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(caminho)


@router.post("/{exame_id}/analisar")
def analisar_exame(
        exame_id: int,
        session: Session = Depends(get_session)
):
    """ Rota para analisar imagens """

    exame = get_exame_image(
        session=session,
        exame_id=exame_id
    )

    if not exame:
        raise HTTPException(
            status_code=404,
            detail="Exame não encontrado"
        )

    upload = exame.upload_imagem[0]
    caminho = upload.caminho_upload

    # task celery (enviando para process_image)
    task = celery_app.send_task(
        "process_image",
        args=[caminho, exame_id]
    )

    return {
        "msg": "Analise iniciada",
        "task_id": task.id
    }


@router.get("/resultado/{task_id}")
def pegar_resultado_analise(
        task_id: str,
        session: Session = Depends(get_session)
):
    resultado = save_result_analise_service(
        task_id=task_id,
        session=session,
        interpretacao=None
    )

    return resultado