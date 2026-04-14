from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import exigir_role, get_session
from app.domains.pacientes.schemas import PacienteCreate, PacientePublic, PacienteUpdate
from app.domains.pacientes.services import (
    create_patient_service,
    delete_patient_service,
    get_patient_service,
    list_patients_service,
    serialize_patient_for_user,
    update_patient_service,
)
from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

RoleProtegida = Annotated[
    Usuario,
    Depends(exigir_role([UserRole.MEDICO, UserRole.SECRETARIA])),
]


@router.post(
    "/",
    response_model=PacientePublic,
    summary="Criar paciente",
    description=(
        "Cria um novo paciente. Secretárias e médicos podem cadastrar pacientes, "
        "mas campos exclusivos do médico só podem ser enviados por usuários com role medico."
    ),
    response_description="Paciente criado com sucesso.",
)
def create_patient(
    patient_in: PacienteCreate,
    user_atual: RoleProtegida,
    session: Session = Depends(get_session),
):
    try:
        patient = create_patient_service(session, patient_in, user_atual)
        session.commit()
        session.refresh(patient)
        return serialize_patient_for_user(patient, user_atual)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar paciente")


@router.get(
    "/",
    response_model=list[PacientePublic],
    summary="Listar pacientes",
    description="Lista os pacientes cadastrados no sistema com visibilidade ajustada pelo perfil do usuário.",
    response_description="Lista de pacientes retornada com sucesso.",
)
def read_patients(
    user_atual: RoleProtegida,
    session: Session = Depends(get_session),
):
    patients = list_patients_service(session)
    return [serialize_patient_for_user(patient, user_atual) for patient in patients]


@router.get(
    "/{patient_id}",
    response_model=PacientePublic,
    summary="Consultar paciente",
    description="Retorna os dados de um paciente específico.",
    response_description="Paciente retornado com sucesso.",
)
def read_patient(
    user_atual: RoleProtegida,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    patient = get_patient_service(session, patient_id)
    return serialize_patient_for_user(patient, user_atual)


@router.put(
    "/{patient_id}",
    response_model=PacientePublic,
    summary="Atualizar paciente",
    description=(
        "Atualiza os dados de um paciente. Secretárias e médicos podem alterar os campos compartilhados. "
        "Campos exclusivos do médico só podem ser alterados por médicos."
    ),
    response_description="Paciente atualizado com sucesso.",
)
def update_patient(
    patient_in: PacienteUpdate,
    user_atual: RoleProtegida,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    try:
        patient = update_patient_service(session, patient_id, patient_in, user_atual)
        session.commit()
        session.refresh(patient)
        return serialize_patient_for_user(patient, user_atual)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar paciente")


@router.delete(
    "/{patient_id}",
    status_code=204,
    summary="Excluir paciente",
    description="Remove um paciente do sistema.",
    responses={204: {"description": "Paciente removido com sucesso."}},
)
def delete_patient(
    _user_atual: RoleProtegida,
    patient_id: int = Path(..., description="Identificador do paciente."),
    session: Session = Depends(get_session),
):
    try:
        delete_patient_service(session, patient_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar paciente")
