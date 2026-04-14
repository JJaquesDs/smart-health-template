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
