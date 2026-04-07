from sqlmodel import Session, create_engine

from app.core.config import settings
from app.core.connection import Base

from app.domains.users.enums import UserRole

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session():
    """ Função para usar em dependências FastAPI """

    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    """ Inicializaa dados inicias com primeiro 'Superusuário' caso não houver """

    from app.domains.users import services as user_service
    from app.domains.users.models import Usuario

    super_user = session.query(Usuario).filter_by(email=settings.FIRST_SUPERUSER).first()  # Verificando se já temos um 'Superusuário'

    if not super_user:
        user_service.create_user_service(session=session, nome="Super Usuario", telefone="000000000",
                                         email=settings.FIRST_SUPERUSER, senha=settings.FIRST_SUPERUSER_PASSWORD,
                                         role=UserRole.SUPERUSER)



