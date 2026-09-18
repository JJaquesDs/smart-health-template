from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository

from app.domains.professionals.secretaria.models import Secretaria


class SecretariaRepository(BaseRepository):
    """ Repository Pattern de 'Secretaria' herdando de 'BaseRepository' """

    def __init__(self):
        """ Inicialização da classe """

        super().__init__(  # Pegando tudo da SuperClasse ou Classe Pai
            model=Secretaria,
            campo_id="secretaria_id"
        )

    def get_by_user_id(self, session: Session, user_id: int):
        """ Método para retornar uma 'Secretaria' pelo 'user_id' """

        return self.get_by_campo(
            session=session,
            campo=Secretaria.usuario_id,
            valor=user_id
        )


# Compatibilidade com os services que ainda usam funcoes de repositorio.
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
