from fastapi import APIRouter, Depends, HTTPException

import traceback

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.deps import (
    get_session,
    exigir_role
)

from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole

from app.domains.users.schemas import (
    UserUpdate
)

from app.domains.professionals.secretaria.schemas import (
    SecretariaPublic,
    SecretariaCreate,
    SecretariaUpdate
)

from app.domains.professionals.secretaria.services import (
    create_secretaria_service,
    update_secretaria_service
)

from app.domains.professionals.secretaria.repository import (
    create_secretaria_db
)

router = APIRouter(prefix="/secretaria", tags=["secretarias"])


@router.post(path="/",
             response_model=SecretariaPublic,
             summary="Criar secretária",
             description="Cria um usuário secretária com role 'secretaria'"
             )
def create_secretaria_route(
        user: SecretariaCreate,
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role([UserRole.ADMIN, UserRole.SUPERUSER]))
):
    """ Rota para criar secretárias """

    try:
        secretaria = create_secretaria_service(
            session=session,
            nome=user.user.nome,
            telefone=user.user.telefone,
            email=user.user.email,
            senha=user.user.senha,
            cpf=user.cpf,
            rg=user.rg,
            role=UserRole.SECRETARIA,
            usuer_atual=user_atual,
        )

        session.commit()

        return secretaria

    except IntegrityError:
        session.rollback()
        print(traceback.format_exc())
        raise HTTPException(
            status_code=400,
            detail="Erro ao salvar usuário"
        )


@router.put(path="/{user_id}", response_model=SecretariaPublic)
def update_secretaria_route(
        user_id: int,
        user_up: UserUpdate,
        sec_up: SecretariaUpdate,
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role([UserRole.ADMIN, UserRole.SUPERUSER]))
):
    """ Rota para atualizar uma Secretária """

    try:
        secretaria = update_secretaria_service(session, user_atual, user_id, user_up, sec_up)
        session.commit()

        return secretaria

    except IntegrityError:
        session.rollback()
        print(traceback.format_exc())

        raise HTTPException(
            status_code=400,
            detail="Não foi possível atualizar a Secretária"
        )
