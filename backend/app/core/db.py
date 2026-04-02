from sqlmodel import Session, create_engine

from app.core.config import settings
from app.core.connection import Base

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_session():
    """ Função para usar em dependências FastAPI """

    with Session(engine) as session:
        yield session


def init_db(session: Session) -> None:
    """ Inicializaa dados inicias (como primeiro admin)"""

    from app.domains.users import service as user_service
    from app.domains.users.models import Usuario

    with Session(engine) as session:

        user = session.query(Usuario).filter_by(email=settings.FIRST_SUPERUSER).first()

        if not user:
            user_service.create_user(
                session=session,
                email=settings.FIRST_SUPERUSER,
                senha=settings.FIRST_SUPERUSER_PASSWORD,
                nome="Super Usuario",
                telefone="000000000",  ## so pra n ter risco de botar um aleatorio kk
                role="admin"
            )



