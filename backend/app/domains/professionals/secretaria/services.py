from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domains.users.models import Usuario
from app.domains.professionals.secretaria.models import Secretaria

from app.domains.users import schemas
from app.domains.professionals.secretaria import schemas

from app.domains.users.enums import UserRole

from app.api.deps import (
    get_session,
    get_current_user_dep,
    exigir_role
)

from app.domains.users.services import (
    unique_email,
    get_user_by_email,
    get_user_by_id,
    get_password_hash,
    create_user_service
)

from app.domains.users.repository import (
    create_user_in_db
)


def create_secretaria_service(
        session: Session,
        nome: str,
        telefone: str,
        email: str,
        senha: str,
        cpf: str,
        rg,
        role: UserRole,
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
            role=UserRole.SECRETARIA
        )

        secretaria = Secretaria(
            user_id=user.usuario_id,
            nome=user.nome,
            cpf=cpf,
            rg=rg,
        )

    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Erro ao criar o usuário secretária"
        )



