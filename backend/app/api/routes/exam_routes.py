from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import exigir_role, get_session
from app.domains.exames.clinicos.schemas import (
    ExameCatalogoCreate,
    ExameCatalogoPublic,
    ExameCatalogoUpdate,
)
from app.domains.exames.clinicos.services import (
    create_exam_catalog_service,
    delete_exam_catalog_service,
    get_exam_catalog_service,
    list_exam_catalog_service,
    update_exam_catalog_service,
)
from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario

router = APIRouter(prefix="/exames", tags=["exames"])


@router.post("/", response_model=ExameCatalogoPublic)
def create_exam(
    exam_in: ExameCatalogoCreate,
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    try:
        exam = create_exam_catalog_service(session, exam_in)
        session.commit()
        session.refresh(exam)
        return exam
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar exame")


@router.get("/", response_model=list[ExameCatalogoPublic])
def read_exams(
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return list_exam_catalog_service(session)


@router.get("/{exam_id}", response_model=ExameCatalogoPublic)
def read_exam(
    exam_id: int,
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return get_exam_catalog_service(session, exam_id)


@router.put("/{exam_id}", response_model=ExameCatalogoPublic)
def update_exam(
    exam_id: int,
    exam_in: ExameCatalogoUpdate,
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    try:
        exam = update_exam_catalog_service(session, exam_id, exam_in)
        session.commit()
        session.refresh(exam)
        return exam
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar exame")


@router.delete("/{exam_id}", status_code=204)
def delete_exam(
    exam_id: int,
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    try:
        delete_exam_catalog_service(session, exam_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar exame")
