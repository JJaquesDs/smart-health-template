from fastapi import HTTPException

import traceback

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domains.users.models import Usuario
from app.domains.professionals.secretaria.models import Secretaria

from app.domains.users.schemas import (
    UserUpdate
)

from app.domains.professionals.secretaria.schemas import (
    SecretariaUpdate
)

from app.domains.professionals.secretaria.repository import (
    create_secretaria_db,
    update_secretaria_db,
    get_secretaria_by_user_id
)

from app.domains.users.enums import UserRole


from app.domains.users.services import (
    create_user_service,
    update_user_service
)


def create_secretaria_service(
        session: Session,
        nome: str,
        telefone: str,
        email: str,
        senha: str,
        cpf: str,
        rg: str,
        role: UserRole.SECRETARIA,
        usuer_atual: Usuario | None = None
):
    """ Service para criar um 'Usuario' Secretáia """

    try:
        user = create_user_service(
            session=session,
            usuer_atual=usuer_atual,
            nome=nome,
            telefone=telefone,
            email=email,
            senha=senha,
            role=role
        )

        # Garantindo do banco o 'usario_id' por ser autoincrement
        session.flush()

        secretaria = Secretaria(
            cpf=cpf,
            rg=rg,
            usuario_id=user.usuario_id
        )

        return create_secretaria_db(session, secretaria)

    except IntegrityError:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=400,
            detail="Erro ao criar o usuário secretária"
        )


def update_secretaria_service(
        session: Session,
        user_atual: Usuario,
        user_id: int,
        user_up: UserUpdate,
        sec_up: SecretariaUpdate
):

    try:
        user = update_user_service(session, user_atual, user_id, user_up)

        secretaria = get_secretaria_by_user_id(session, user_id)

        if not secretaria:
            raise HTTPException(
                status_code=404,
                detail="Secretária não encontrada"
            )

        for chave, valor in sec_up.model_dump(exclude_unset=True).items():
            setattr(secretaria, chave, valor)

        return update_secretaria_db(session, secretaria)

    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Não foi possível atualizar secretária"
        )



