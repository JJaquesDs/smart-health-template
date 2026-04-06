from  sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.users.models import Usuario


def get_user_by_id(session: Session, user_id: int) -> Usuario | None:  # Pode retornar ou não um Usuario
    """ Função que retorna consulta com o 'id' """

    return session.query(Usuario).filter_by(usuario_id=user_id).first()


def get_user_by_email(session: Session, email: str) -> Usuario | None:  # Pode retornar ou não um Usuario
    """ Função que retorna consulta com 'email' """

    return session.query(Usuario).filter_by(email=email).first()


def create_user_in_db(session: Session, user: Usuario) -> Usuario:
    """ Função que instância um Usuario no banco de dados """

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_all_users_in_db(session: Session) -> list[Usuario]:  # Retorna uma lista de Usuario
    """ Função que retorna todos os Usuarios"""

    resultado = session.execute(select(Usuario))
    return resultado.scalars().all()


def delete_user_in_db(session: Session, user: Usuario) -> None:
    """ Função que deleta um Usuario no banco de dados """

    session.delete(user)
    session.commit()


def update_user_in_db(session: Session, user) -> Usuario:
    """ Função que atualiza um Usuario no banco de dados """

    session.commit()
    session.refresh(user)

    return user
