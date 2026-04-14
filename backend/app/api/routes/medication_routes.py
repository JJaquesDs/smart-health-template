from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import exigir_role, get_session
from app.domains.medicamentos.schemas import (
    MedicamentoCatalogoCreate,
    MedicamentoCatalogoPublic,
    MedicamentoCatalogoUpdate,
)
from app.domains.medicamentos.services import (
    create_medication_catalog_service,
    delete_medication_catalog_service,
    get_medication_catalog_service,
    list_medication_catalog_service,
    update_medication_catalog_service,
)
from app.domains.users.enums import UserRole
from app.domains.users.models import Usuario

router = APIRouter(prefix="/medicamentos", tags=["medicamentos"])


@router.post(
    "/",
    response_model=MedicamentoCatalogoPublic,
    summary="Criar medicamento de catálogo",
    description=(
        "Cria um novo medicamento no catálogo principal do sistema. "
        "Disponível para médicos, administradores e superusuários autenticados."
    ),
    response_description="Medicamento criado com sucesso.",
    responses={
        400: {"description": "Erro de integridade ou dados inválidos ao criar o medicamento."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
    },
)
def create_medication(
    medication_in: MedicamentoCatalogoCreate,
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    try:
        medication = create_medication_catalog_service(session, medication_in)
        session.commit()
        session.refresh(medication)
        return medication
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar medicamento")


@router.get(
    "/",
    response_model=list[MedicamentoCatalogoPublic],
    summary="Listar medicamentos de catálogo",
    description="Retorna todos os medicamentos cadastrados no catálogo do sistema.",
    response_description="Lista de medicamentos retornada com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
    },
)
def read_medications(
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return list_medication_catalog_service(session)


@router.get(
    "/{medication_id}",
    response_model=MedicamentoCatalogoPublic,
    summary="Consultar medicamento de catálogo",
    description="Retorna os dados de um medicamento específico do catálogo.",
    response_description="Medicamento retornado com sucesso.",
    responses={
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
        404: {"description": "Medicamento não encontrado."},
    },
)
def read_medication(
    medication_id: int = Path(..., description="Identificador do medicamento no catálogo."),
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return get_medication_catalog_service(session, medication_id)


@router.put(
    "/{medication_id}",
    response_model=MedicamentoCatalogoPublic,
    summary="Atualizar medicamento de catálogo",
    description="Atualiza os dados de um medicamento já existente no catálogo.",
    response_description="Medicamento atualizado com sucesso.",
    responses={
        400: {
            "description": "Erro de integridade ou dados inválidos ao atualizar o medicamento."
        },
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
        404: {"description": "Medicamento não encontrado."},
    },
)
def update_medication(
    medication_in: MedicamentoCatalogoUpdate,
    medication_id: int = Path(..., description="Identificador do medicamento no catálogo."),
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    try:
        medication = update_medication_catalog_service(session, medication_id, medication_in)
        session.commit()
        session.refresh(medication)
        return medication
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao atualizar medicamento")


@router.delete(
    "/{medication_id}",
    status_code=204,
    summary="Excluir medicamento de catálogo",
    description="Remove um medicamento do catálogo do sistema.",
    responses={
        204: {"description": "Medicamento removido com sucesso."},
        400: {"description": "Erro ao remover o medicamento."},
        401: {"description": "Usuário não autenticado."},
        403: {"description": "Usuário sem permissão para acessar o catálogo."},
        404: {"description": "Medicamento não encontrado."},
    },
)
def delete_medication(
    medication_id: int = Path(..., description="Identificador do medicamento no catálogo."),
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    try:
        delete_medication_catalog_service(session, medication_id)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Erro ao deletar medicamento")
