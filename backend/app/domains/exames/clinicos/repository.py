from sqlalchemy.orm import Session

from app.domains.exames.clinicos.models import ExameCatalogo


def create_exam_catalog_db(session: Session, exam: ExameCatalogo) -> ExameCatalogo:
    session.add(exam)
    return exam


def get_exam_catalog_by_id(session: Session, exam_id: int) -> ExameCatalogo | None:
    return session.query(ExameCatalogo).filter_by(exame_id=exam_id).first()


def get_exam_catalog_by_name(session: Session, nome: str) -> ExameCatalogo | None:
    return session.query(ExameCatalogo).filter_by(nome=nome).first()


def list_exam_catalog_db(session: Session) -> list[ExameCatalogo]:
    return session.query(ExameCatalogo).order_by(ExameCatalogo.nome.asc()).all()


def update_exam_catalog_db(session: Session, exam: ExameCatalogo) -> ExameCatalogo:
    return exam


def delete_exam_catalog_db(session: Session, exam: ExameCatalogo) -> None:
    session.delete(exam)
