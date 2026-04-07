from fastapi import HTTPException

import traceback

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domains.users.models import Usuario
from app.domains.professionals.secretaria.models import Secretaria

from app.domains.users import schemas
from app.domains.professionals.secretaria import schemas

from app.domains.professionals.secretaria.repository import (
    create_secretaria_db
)

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
    create_user_service,
    is_admin_or_superuser
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



