import traceback

from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domains.professionals.medico.especialidade.models import Especialidade

from app.domains.professionals.medico.especialidade.repository import (
    create_esp_db,
    get_esp_db,
    get_all_esp_in_db
)


def titulo_formatado(titulo: str) -> str:
    """ Função para padronizar o título e evitar inconsistências no banco"""

    titulo_format = titulo.strip().title()

    return titulo_format


def create_esp_service(
        session: Session,
        titulo: str
):
    try:

        titulo_format = titulo_formatado(titulo=titulo)

        get_titulo = get_esp_db(session, titulo=titulo_format)

        # Se já houver uma especialidade com esse título, não deixa o usuário instânciar (evitar redundância)
        if get_titulo:
            raise HTTPException(
                status_code=400,
                detail="Especialidade já existe no banco de dados"
            )

        # Se não houver, criamos a nova especialidade
        especialidade = Especialidade(
            titulo=titulo_format
        )

        create_esp_db(session, especialidade)

        return especialidade

    except IntegrityError:
        print(traceback.format_exc())

        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar a Especialidade"
        )


def get_all_esp_service(session: Session) -> list[Especialidade] | None:
    """ Service para listar especialidades"""

    return get_all_esp_in_db(session)
