from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository

from app.domains.professionals.medico.especialidade.models import Especialidade


class EspecialidadeRepository(BaseRepository):
    """ Repository Pattern de 'Especialidade' herdando de 'BaseRepository' """

    def __init__(self):
        """ Inicialização da classe """

        super().__init__(  # Pegando tudo da SuperClasse ou Classe Pai
            model=Especialidade,
            campo_id="esp_id"
        )

    def get_by_titulo(self, session: Session, titulo: str):
        """ Método para retornar uma 'Especialidade' pelo campo 'titulo' """

        return self.get_by_campo(
            session=session,
            campo=Especialidade.titulo,
            valor=titulo
        )
