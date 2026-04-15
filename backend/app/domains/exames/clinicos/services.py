from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domains.exames.clinicos.models import ExameCatalogo
from app.domains.exames.clinicos.repository import (
    create_exam_catalog_db,
    delete_exam_catalog_db,
    get_exam_catalog_by_id,
    get_exam_catalog_by_name,
    list_exam_catalog_db,
    update_exam_catalog_db,
)
from app.domains.exames.clinicos.schemas import ExameCatalogoCreate, ExameCatalogoUpdate


def create_exam_catalog_service(
    session: Session,
    exam_in: ExameCatalogoCreate,
) -> ExameCatalogo:
    if get_exam_catalog_by_name(session, exam_in.nome):
        raise HTTPException(status_code=400, detail="Exame já cadastrado")

    exam = ExameCatalogo(**exam_in.model_dump())
    return create_exam_catalog_db(session, exam)


def list_exam_catalog_service(session: Session) -> list[ExameCatalogo]:
    return list_exam_catalog_db(session)


def get_exam_catalog_service(session: Session, exam_id: int) -> ExameCatalogo:
    exam = get_exam_catalog_by_id(session, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exame não encontrado")
    return exam


def update_exam_catalog_service(
    session: Session,
    exam_id: int,
    exam_in: ExameCatalogoUpdate,
) -> ExameCatalogo:
    exam = get_exam_catalog_service(session, exam_id)
    update_data = exam_in.model_dump(exclude_unset=True)

    if "nome" in update_data:
        existing_exam = get_exam_catalog_by_name(session, update_data["nome"])
        if existing_exam and existing_exam.exame_id != exam_id:
            raise HTTPException(status_code=400, detail="Já existe um exame com esse nome")

    for key, value in update_data.items():
        setattr(exam, key, value)

    return update_exam_catalog_db(session, exam)


def delete_exam_catalog_service(session: Session, exam_id: int) -> None:
    exam = get_exam_catalog_service(session, exam_id)
    delete_exam_catalog_db(session, exam)
