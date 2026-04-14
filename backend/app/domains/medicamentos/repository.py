from sqlalchemy.orm import Session

from app.domains.medicamentos.models import MedicamentoCatalogo


def create_medication_catalog_db(
    session: Session,
    medication: MedicamentoCatalogo,
) -> MedicamentoCatalogo:
    session.add(medication)
    return medication


def get_medication_catalog_by_id(
    session: Session,
    medication_id: int,
) -> MedicamentoCatalogo | None:
    return session.query(MedicamentoCatalogo).filter_by(medicamento_id=medication_id).first()


def get_medication_catalog_by_name(
    session: Session,
    nome: str,
) -> MedicamentoCatalogo | None:
    return session.query(MedicamentoCatalogo).filter_by(nome=nome).first()


def list_medication_catalog_db(session: Session) -> list[MedicamentoCatalogo]:
    return session.query(MedicamentoCatalogo).order_by(MedicamentoCatalogo.nome.asc()).all()


def update_medication_catalog_db(
    session: Session,
    medication: MedicamentoCatalogo,
) -> MedicamentoCatalogo:
    return medication


def delete_medication_catalog_db(session: Session, medication: MedicamentoCatalogo) -> None:
    session.delete(medication)
