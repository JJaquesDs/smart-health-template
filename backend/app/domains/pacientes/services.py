from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domains.pacientes.models import Paciente
from app.domains.pacientes.repository import (
    create_patient_db,
    delete_patient_db,
    get_patient_by_cpf,
    get_patient_by_email,
    get_patient_by_id,
    list_patients_db,
)
from app.domains.pacientes.schemas import PacienteCreate, PacienteUpdate
from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario


DOCTOR_ONLY_FIELDS = {"medicamentos", "historico_medico", "observacoes"}


def _validate_doctor_only_fields(user: Usuario, data: dict) -> None:
    if user.role == UserRole.MEDICO:
        return

    forbidden_fields = [
        field for field in DOCTOR_ONLY_FIELDS if field in data and data[field] not in (None, "")
    ]
    if forbidden_fields:
        raise HTTPException(
            status_code=403,
            detail="Usuário sem permissão para alterar campos exclusivos do médico",
        )


def _validate_unique_fields(
    session: Session,
    cpf: str | None = None,
    email: str | None = None,
    patient_id: int | None = None,
) -> None:
    if cpf:
        existing_patient = get_patient_by_cpf(session, cpf)
        if existing_patient and existing_patient.paciente_id != patient_id:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    if email:
        existing_patient = get_patient_by_email(session, email)
        if existing_patient and existing_patient.paciente_id != patient_id:
            raise HTTPException(status_code=400, detail="Email já cadastrado")


def serialize_patient_for_user(patient: Paciente, user: Usuario) -> dict:
    data = {
        "paciente_id": patient.paciente_id,
        "nome": patient.nome,
        "cpf": patient.cpf,
        "data_nascimento": patient.data_nascimento,
        "genero": patient.genero,
        "email": patient.email,
        "telefone": patient.telefone,
        "rua": patient.rua,
        "numero": patient.numero,
        "complemento": patient.complemento,
        "cidade": patient.cidade,
        "estado": patient.estado,
        "cep": patient.cep,
        "dados_clinicos": patient.dados_clinicos,
        "tipo_sanguineo": patient.tipo_sanguineo,
        "ultimo_exame": patient.ultimo_exame,
        "alergias": patient.alergias,
        "medicamentos": patient.medicamentos,
        "historico_medico": patient.historico_medico,
        "observacoes": patient.observacoes,
        "contato_emergencia_nome": patient.contato_emergencia_nome,
        "contato_emergencia_parentesco": patient.contato_emergencia_parentesco,
        "contato_emergencia_telefone": patient.contato_emergencia_telefone,
    }

    if user.role == UserRole.SECRETARIA:
        data["medicamentos"] = None
        data["historico_medico"] = None
        data["observacoes"] = None

    return data


def create_patient_service(session: Session, patient_in: PacienteCreate, user: Usuario) -> Paciente:
    data = patient_in.model_dump()
    _validate_doctor_only_fields(user, data)
    _validate_unique_fields(session, cpf=data["cpf"], email=data["email"])
    patient = Paciente(**data)
    return create_patient_db(session, patient)


def list_patients_service(session: Session) -> list[Paciente]:
    return list_patients_db(session)


def get_patient_service(session: Session, patient_id: int) -> Paciente:
    patient = get_patient_by_id(session, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return patient


def update_patient_service(
    session: Session,
    patient_id: int,
    patient_in: PacienteUpdate,
    user: Usuario,
) -> Paciente:
    patient = get_patient_service(session, patient_id)
    update_data = patient_in.model_dump(exclude_unset=True)
    _validate_doctor_only_fields(user, update_data)
    _validate_unique_fields(
        session,
        cpf=update_data.get("cpf"),
        email=update_data.get("email"),
        patient_id=patient_id,
    )

    for key, value in update_data.items():
        setattr(patient, key, value)

    return patient


def delete_patient_service(session: Session, patient_id: int) -> None:
    patient = get_patient_service(session, patient_id)
    delete_patient_db(session, patient)
