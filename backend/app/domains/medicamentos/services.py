from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.domains.medicamentos.models import MedicamentoCatalogo
from app.domains.medicamentos.repository import (
    create_medication_catalog_db,
    delete_medication_catalog_db,
    get_medication_catalog_by_id,
    get_medication_catalog_by_name,
    list_medication_catalog_db,
    update_medication_catalog_db,
)
from app.domains.medicamentos.schemas import (
    MedicamentoCatalogoCreate,
    MedicamentoCatalogoUpdate,
)


def create_medication_catalog_service(
    session: Session,
    medication_in: MedicamentoCatalogoCreate,
) -> MedicamentoCatalogo:
    if get_medication_catalog_by_name(session, medication_in.nome):
        raise HTTPException(status_code=400, detail="Medicamento já cadastrado")

    medication = MedicamentoCatalogo(**medication_in.model_dump())
    return create_medication_catalog_db(session, medication)


def list_medication_catalog_service(session: Session) -> list[MedicamentoCatalogo]:
    return list_medication_catalog_db(session)


def get_medication_catalog_service(
    session: Session,
    medication_id: int,
) -> MedicamentoCatalogo:
    medication = get_medication_catalog_by_id(session, medication_id)
    if not medication:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    return medication


def update_medication_catalog_service(
    session: Session,
    medication_id: int,
    medication_in: MedicamentoCatalogoUpdate,
) -> MedicamentoCatalogo:
    medication = get_medication_catalog_service(session, medication_id)
    update_data = medication_in.model_dump(exclude_unset=True)

    if "nome" in update_data:
        existing_medication = get_medication_catalog_by_name(session, update_data["nome"])
        if existing_medication and existing_medication.medicamento_id != medication_id:
            raise HTTPException(status_code=400, detail="Já existe um medicamento com esse nome")

    for key, value in update_data.items():
        setattr(medication, key, value)

    return update_medication_catalog_db(session, medication)


def delete_medication_catalog_service(session: Session, medication_id: int) -> None:
    medication = get_medication_catalog_service(session, medication_id)
    delete_medication_catalog_db(session, medication)
