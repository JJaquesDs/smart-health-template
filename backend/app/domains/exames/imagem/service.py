import os
import shutil

from celery.result import AsyncResult

from fastapi import UploadFile, HTTPException

from sqlalchemy.orm import Session

from app.domains.exames.imagem.models import UploadExameImagem, ExameImagem, ResultadoExameImagemIa

from app.domains.exames.imagem.repository import (
    save_upload_image,
    save_exam_image,
    get_resultado_analise_exame_img,
    save_result_analise_exame_img
)

UPLOAD_DIR = "uploads/"

BASE_URL = "http://localhost:8000"


def create_exam_with_upload(
        session: Session,
        file: UploadFile,
        tipo: str,
        descricao: str | None = None
):
    """" Service para Salvar e fazer Upload de Exame Imagem """

    # Salvando arquivo(upload)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    pacote_file = os.path.join(UPLOAD_DIR, file.filename)

    with open(pacote_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_url = f"{BASE_URL}/uploads/{file.filename}"

    # Criando o Exame
    exame = ExameImagem(
        tipo=tipo,
        descricao=descricao,
        link_imagem=file_url
    )

    save_exam_image(
        session=session,
        exame=exame
    )

    session.flush()

    # Salvando upload vinculado ao exame

    upload = UploadExameImagem(
        titulo=file.filename,
        caminho_upload=pacote_file,
        exame_imagem_id=exame.exame_id
    )

    save_upload_image(
        session=session,
        upload=upload
    )

    session.flush()

    return exame, upload

from celery.result import AsyncResult
from app.core.celery_client import celery_app


def save_result_analise_service(
        task_id: str,
        session: Session,
        interpretacao: str | None = None
):
    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.state == "PENDING":
        return {"status": "PENDING"}

    if task_result.state == "FAILURE":
        return {"status": "FAILURE"}

    if task_result.state == "SUCCESS":
        dados = task_result.result

        # evitar duplicação
        existente = get_resultado_analise_exame_img(
            session=session,
            exame_imagem_id=dados["exame_img_id"]
        )

        if existente:
            return existente  # já salvo

        resultado = ResultadoExameImagemIa(
            classe_predita=dados["classe"],
            confianca=dados["confianca"],
            probabilidades=dados["lista"],
            interpretacao=interpretacao,
            exame_imagem_id=dados["exame_img_id"]
        )

        save_result_analise_exame_img(session=session, resultado=resultado)
        session.commit()

        return resultado
