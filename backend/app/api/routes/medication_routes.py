from fastapi import APIRouter, Depends, HTTPException
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


@router.post("/", response_model=MedicamentoCatalogoPublic)
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


@router.get("/", response_model=list[MedicamentoCatalogoPublic])
def read_medications(
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return list_medication_catalog_service(session)


@router.get("/{medication_id}", response_model=MedicamentoCatalogoPublic)
def read_medication(
    medication_id: int,
    session: Session = Depends(get_session),
    _user_atual: Usuario = Depends(
        exigir_role([UserRole.MEDICO, UserRole.ADMIN, UserRole.SUPERUSER])
    ),
):
    return get_medication_catalog_service(session, medication_id)


@router.put("/{medication_id}", response_model=MedicamentoCatalogoPublic)
def update_medication(
    medication_id: int,
    medication_in: MedicamentoCatalogoUpdate,
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


@router.delete("/{medication_id}", status_code=204)
def delete_medication(
    medication_id: int,
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
