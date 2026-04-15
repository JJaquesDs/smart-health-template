from fastapi import APIRouter, Depends, HTTPException, Path
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


@router.post(
    "/",
    response_model=ExameCatalogoPublic,
    summary="Criar exame de catálogo",
    description=(
        "Cria um novo exame no catálogo principal do sistema. "
        "Disponível para médicos, administradores e superusuários autenticados."
    ),
    response_description="Exame criado com sucesso.",
    responses={
        400: {"description": "Erro de integridade ou dados inválidos ao criar o exame."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
    },
)
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


@router.get(
    "/",
    response_model=list[ExameCatalogoPublic],
    summary="Listar exames de catálogo",
    description="Retorna todos os exames cadastrados no catálogo do sistema.",
    response_description="Lista de exames retornada com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
    },
)
def read_exams(
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return list_exam_catalog_service(session)


@router.get(
    "/{exam_id}",
    response_model=ExameCatalogoPublic,
    summary="Consultar exame de catálogo",
    description="Retorna os dados de um exame específico do catálogo.",
    response_description="Exame retornado com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
        404: {"description": "Exame não encontrado."},
    },
)
def read_exam(
    exam_id: int = Path(..., description="Identificador do exame no catálogo."),
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return get_exam_catalog_service(session, exam_id)


@router.put(
    "/{exam_id}",
    response_model=ExameCatalogoPublic,
    summary="Atualizar exame de catálogo",
    description="Atualiza os dados de um exame já existente no catálogo.",
    response_description="Exame atualizado com sucesso.",
    responses={
        400: {"description": "Erro de integridade ou dados inválidos ao atualizar o exame."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
        404: {"description": "Exame não encontrado."},
    },
)
def update_exam(
    exam_in: ExameCatalogoUpdate,
    exam_id: int = Path(..., description="Identificador do exame no catálogo."),
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


@router.delete(
    "/{exam_id}",
    status_code=204,
    summary="Excluir exame de catálogo",
    description="Remove um exame do catálogo do sistema.",
    responses={
        204: {"description": "Exame removido com sucesso."},
        400: {"description": "Erro ao remover o exame."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
        404: {"description": "Exame não encontrado."},
    },
)
def delete_exam(
    exam_id: int = Path(..., description="Identificador do exame no catálogo."),
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
