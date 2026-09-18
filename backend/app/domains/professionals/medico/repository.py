from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository

from app.domains.professionals.medico.models import Medico


class MedicoRepository(BaseRepository):
    """ Repository Pattern de 'Medico' herdando de 'BaseRepository' """

    def __init__(self):
        """ Inicialização da classe """

        super().__init__(  # Pegando tudo da SuperClasse ou Classe Pai
            model=Medico,
            campo_id="medico_id"
        )

    def get_by_user_id(self, session: Session, user_id: int):
        """ Método para retornar uma 'Medico' pelo 'user_id' """

        return self.get_by_campo(
            session=session,
            campo=Medico.usuario_id,
            valor=user_id
        )


# Compatibilidade com os services que ainda usam funcoes de repositorio.
def create_medico_db(session: Session, medico: Medico):
    """ Função que instância 'medico' no banco de dados """

    session.add(medico)

    return medico


def get_medico_by_user_id(session: Session, user_id: int) -> Medico | None:
    return session.query(Medico).filter_by(usuario_id=user_id).first()
