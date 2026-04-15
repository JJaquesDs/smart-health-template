from sqlalchemy.orm import Session

from app.domains.pacientes.models import (
    Paciente,
    PacienteExame,
    PacienteHistoricoClinico,
    PacienteMedicamento,
)


def create_patient_db(session: Session, patient: Paciente) -> Paciente:
    session.add(patient)
    return patient


def get_patient_by_id(session: Session, patient_id: int) -> Paciente | None:
    return session.query(Paciente).filter_by(paciente_id=patient_id).first()


def get_patient_by_cpf(session: Session, cpf: str) -> Paciente | None:
    return session.query(Paciente).filter_by(cpf=cpf).first()


def get_patient_by_email(session: Session, email: str) -> Paciente | None:
    return session.query(Paciente).filter_by(email=email).first()


def list_patients_db(session: Session) -> list[Paciente]:
    return session.query(Paciente).order_by(Paciente.nome.asc()).all()


def delete_patient_db(session: Session, patient: Paciente) -> None:
    session.delete(patient)


def create_patient_history_db(
    session: Session,
    history: PacienteHistoricoClinico,
) -> PacienteHistoricoClinico:
    session.add(history)
    return history


def list_patient_histories_db(session: Session, patient_id: int) -> list[PacienteHistoricoClinico]:
    return (
        session.query(PacienteHistoricoClinico)
        .filter_by(paciente_id=patient_id)
        .order_by(PacienteHistoricoClinico.data_registro.desc())
        .all()
    )


def get_patient_history_by_id(
    session: Session,
    patient_id: int,
    history_id: int,
) -> PacienteHistoricoClinico | None:
    return (
        session.query(PacienteHistoricoClinico)
        .filter_by(paciente_id=patient_id, historico_id=history_id)
        .first()
    )


def delete_patient_history_db(session: Session, history: PacienteHistoricoClinico) -> None:
    session.delete(history)


def create_patient_exam_db(session: Session, exam: PacienteExame) -> PacienteExame:
    session.add(exam)
    return exam


def list_patient_exams_db(session: Session, patient_id: int) -> list[PacienteExame]:
    return (
        session.query(PacienteExame)
        .filter_by(paciente_id=patient_id)
        .order_by(PacienteExame.data_exame.desc())
        .all()
    )


def get_patient_exam_by_id(
    session: Session,
    patient_id: int,
    exam_id: int,
) -> PacienteExame | None:
    return (
        session.query(PacienteExame)
        .filter_by(paciente_id=patient_id, paciente_exame_id=exam_id)
        .first()
    )


def delete_patient_exam_db(session: Session, exam: PacienteExame) -> None:
    session.delete(exam)


def create_patient_medication_db(
    session: Session,
    medication: PacienteMedicamento,
) -> PacienteMedicamento:
    session.add(medication)
    return medication


def list_patient_medications_db(session: Session, patient_id: int) -> list[PacienteMedicamento]:
    return (
        session.query(PacienteMedicamento)
        .filter_by(paciente_id=patient_id)
        .order_by(PacienteMedicamento.paciente_medicamento_id.desc())
        .all()
    )


def get_patient_medication_by_id(
    session: Session,
    patient_id: int,
    medication_id: int,
) -> PacienteMedicamento | None:
    return (
        session.query(PacienteMedicamento)
        .filter_by(paciente_id=patient_id, paciente_medicamento_id=medication_id)
        .first()
    )


def delete_patient_medication_db(
    session: Session,
    medication: PacienteMedicamento,
) -> None:
    session.delete(medication)
