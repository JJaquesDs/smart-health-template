from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domains.pacientes.models import Paciente
from app.domains.pacientes.repository import (
    create_patient_db,
    create_patient_exam_db,
    create_patient_history_db,
    create_patient_medication_db,
    delete_patient_exam_db,
    delete_patient_history_db,
    delete_patient_medication_db,
    delete_patient_db,
    get_patient_by_cpf,
    get_patient_by_email,
    get_patient_exam_by_id,
    get_patient_history_by_id,
    get_patient_by_id,
    get_patient_medication_by_id,
    list_patients_db,
    list_patient_exams_db,
    list_patient_histories_db,
    list_patient_medications_db,
)
from app.domains.pacientes.schemas import PacienteCreate, PacienteUpdate
from app.domains.pacientes.models import (
    PacienteExame,
    PacienteHistoricoClinico,
    PacienteMedicamento,
)
from app.domains.pacientes.schemas import (
    PacienteExameCreate,
    PacienteExameUpdate,
    PacienteHistoricoClinicoCreate,
    PacienteHistoricoClinicoUpdate,
    PacienteMedicamentoCreate,
    PacienteMedicamentoUpdate,
)
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


def list_patient_histories_service(
    session: Session,
    patient_id: int,
) -> list[PacienteHistoricoClinico]:
    get_patient_service(session, patient_id)
    return list_patient_histories_db(session, patient_id)


def get_patient_history_service(
    session: Session,
    patient_id: int,
    history_id: int,
) -> PacienteHistoricoClinico:
    get_patient_service(session, patient_id)
    history = get_patient_history_by_id(session, patient_id, history_id)
    if not history:
      raise HTTPException(status_code=404, detail="Histórico clínico não encontrado")
    return history


def create_patient_history_service(
    session: Session,
    patient_id: int,
    history_in: PacienteHistoricoClinicoCreate,
) -> PacienteHistoricoClinico:
    get_patient_service(session, patient_id)
    history = PacienteHistoricoClinico(
        paciente_id=patient_id,
        **history_in.model_dump(),
    )
    return create_patient_history_db(session, history)


def update_patient_history_service(
    session: Session,
    patient_id: int,
    history_id: int,
    history_in: PacienteHistoricoClinicoUpdate,
) -> PacienteHistoricoClinico:
    history = get_patient_history_service(session, patient_id, history_id)
    for key, value in history_in.model_dump(exclude_unset=True).items():
        setattr(history, key, value)
    return history


def delete_patient_history_service(session: Session, patient_id: int, history_id: int) -> None:
    history = get_patient_history_service(session, patient_id, history_id)
    delete_patient_history_db(session, history)


def list_patient_exams_service(session: Session, patient_id: int) -> list[PacienteExame]:
    get_patient_service(session, patient_id)
    return list_patient_exams_db(session, patient_id)


def get_patient_exam_service(
    session: Session,
    patient_id: int,
    exam_id: int,
) -> PacienteExame:
    get_patient_service(session, patient_id)
    exam = get_patient_exam_by_id(session, patient_id, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exame do paciente não encontrado")
    return exam


def create_patient_exam_service(
    session: Session,
    patient_id: int,
    exam_in: PacienteExameCreate,
) -> PacienteExame:
    get_patient_service(session, patient_id)
    exam = PacienteExame(paciente_id=patient_id, **exam_in.model_dump())
    return create_patient_exam_db(session, exam)


def update_patient_exam_service(
    session: Session,
    patient_id: int,
    exam_id: int,
    exam_in: PacienteExameUpdate,
) -> PacienteExame:
    exam = get_patient_exam_service(session, patient_id, exam_id)
    for key, value in exam_in.model_dump(exclude_unset=True).items():
        setattr(exam, key, value)
    return exam


def delete_patient_exam_service(session: Session, patient_id: int, exam_id: int) -> None:
    exam = get_patient_exam_service(session, patient_id, exam_id)
    delete_patient_exam_db(session, exam)


def list_patient_medications_service(
    session: Session,
    patient_id: int,
) -> list[PacienteMedicamento]:
    get_patient_service(session, patient_id)
    return list_patient_medications_db(session, patient_id)


def get_patient_medication_service(
    session: Session,
    patient_id: int,
    medication_id: int,
) -> PacienteMedicamento:
    get_patient_service(session, patient_id)
    medication = get_patient_medication_by_id(session, patient_id, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medicamento do paciente não encontrado")
    return medication


def create_patient_medication_service(
    session: Session,
    patient_id: int,
    medication_in: PacienteMedicamentoCreate,
) -> PacienteMedicamento:
    get_patient_service(session, patient_id)
    medication = PacienteMedicamento(
        paciente_id=patient_id,
        **medication_in.model_dump(),
    )
    return create_patient_medication_db(session, medication)


def update_patient_medication_service(
    session: Session,
    patient_id: int,
    medication_id: int,
    medication_in: PacienteMedicamentoUpdate,
) -> PacienteMedicamento:
    medication = get_patient_medication_service(session, patient_id, medication_id)
    for key, value in medication_in.model_dump(exclude_unset=True).items():
        setattr(medication, key, value)
    return medication


def delete_patient_medication_service(
    session: Session,
    patient_id: int,
    medication_id: int,
) -> None:
    medication = get_patient_medication_service(session, patient_id, medication_id)
    delete_patient_medication_db(session, medication)
