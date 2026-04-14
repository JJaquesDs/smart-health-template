from sqlalchemy.orm import Session

from app.domains.pacientes.models import Paciente


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
