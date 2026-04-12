from sqlalchemy.orm import Session

from app.domains.professionals.medico.models import Medico

from app.domains.users.repository import (
    get_user_by_id,
    get_user_by_email,
)


def create_medico_db(session: Session, medico: Medico):
    """ Função que instância 'medico' no banco de dados """

    session.add(medico)

    return medico


def get_medico_by_user_id(session: Session, medico_id: int) -> Medico | None:
    """ Função que consulta um médico pelo 'user_id' """

    return session.query(Medico).filter_by(user_id=Medico.medico_id).first()
