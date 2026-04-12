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


def get_secretaria_by_user_id(session: Session, user_id: int) -> Secretaria | None:  # Pode retornar ou não um Usuario
    """ Função que retorna consulta com o 'id' """

    return session.query(Secretaria).filter_by(usuario_id=user_id).first()


def update_secretaria_db(session: Session, user) -> Secretaria:
    """ Função que atualiza uma secretaria no db"""

    # Aqui apenas retornamos o 'Usuario' porque o parâmetro 'session' do SqlAlchemy já detecta automaticamente mudanças nos dados

    return user

