import traceback

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domains.users.models import Usuario
from app.domains.users.enums import UserRole

from app.domains.professionals.medico.schemas import (
    MedicoPublic,
    MedicoCreate
)

from app.domains.professionals.medico.services import (
    create_medico_service
)

from app.domains.professionals.medico.especialidade.esp_schemas import (
    EspecialidadePublic,
    EspecialidadeCreate
)

from app.api.deps import (
    exigir_role,
    get_session
)

router = APIRouter(prefix="/medico", tags=["medicos"])


@router.post(
            path="/",
            response_model=MedicoPublic,
            summary="Criar Médico",
            description="Cria um usuário médico com role 'medico'"
)
def create_medico_route(
        medico_novo: MedicoCreate,
        session: Session = Depends(get_session),
        user_atual: Usuario = Depends(exigir_role(roles=[UserRole.ADMIN, UserRole.SUPERUSER]))
):
    """ Rota para criar médicos """

    medico = create_medico_service(
        session=session,
        nome=medico_novo.user.nome,
        telefone=medico_novo.user.telefone,
        email=medico_novo.user.email,
        senha=medico_novo.user.senha,
        cpf=medico_novo.cpf,
        rg=medico_novo.rg,
        crm_num=medico_novo.crm_numero,
        crm_uf=medico_novo.crm_UF,
        role=UserRole.MEDICO,
        med_esps=medico_novo.med_esps,
        user_atual=user_atual
    )

    session.commit()

    return medico

