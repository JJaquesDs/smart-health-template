import traceback

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.deps import (
    get_session,
    exigir_role
)

from app.domains.users.models import Usuario

from app.domains.users.enums import UserRole

from app.domains.professionals.medico.especialidade.models import Especialidade

from app.domains.professionals.medico.especialidade.esp_schemas import (
    EspecialidadePublic,
    EspecialidadeCreate
)

from app.domains.professionals.medico.especialidade.services import (
    create_esp_service,
    get_all_esp_service
)


router = APIRouter(prefix="/medico/esp", tags=["especialidades"])


@router.post(
    path="/",
    summary="Criar Especialidade",
    response_model=EspecialidadePublic,
    description="Rota para criar especialidade médica (deve ser chamada antes de criar médicos)",
)
def create_esp_route(
    especialidade: EspecialidadeCreate,
    session: Session = Depends(get_session),
    user_atual: Usuario = Depends(exigir_role(roles=[UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER]))
):
    try:
        especialidade = create_esp_service(
            session=session,
            titulo=especialidade.titulo
        )

        session.commit()

        return especialidade

    except IntegrityError:
        session.rollback()
        print(traceback.format_exc())

        raise HTTPException(
            status_code=400,
            detail="Erro ao criar Especialidade"
        )


@router.get(
    path="/read_esps",
    response_model=list[EspecialidadePublic],
    description="Rota para listar todas as Especialidades (usada para o médico vizualizar se a sua já está criada"
)
def get_all_esp_route(
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role(roles=[UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER]))
):
    """ Rota para vizualizar todos as 'Especialidades' """

    return get_all_esp_service(session)

