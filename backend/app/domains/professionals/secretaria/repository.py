from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.professionals.secretaria.models import Secretaria

from app.domains.users.repository import (
    get_user_by_id,
    get_user_by_email,
)


def create_secretaria_db(session: Session, secretaria: Secretaria):
    """ Função que instância no db (mas n valida nem commita)"""

    session.add(secretaria)

    return secretaria