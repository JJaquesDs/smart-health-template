from sqlalchemy.orm import Session

from app.domains.users.models import Usuario

from app.core.base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    """ Repository Pattern de 'Usuário' herdando de 'BaseRepository' """

    def __init__(self):
        """ Inicialização da classe """

        super().__init__(  # Pegando tudo da SuperClasse ou Classe Pai
            model=Usuario,
            campo_id="usuario_id"
        )

    def get_by_email(self, session: Session, email: str):
        """ Método para consultar por 'email' (Reutilizando get_by_campo como o campo sendo 'email') """

        return self.get_by_campo(
            session=session,
            campo=Usuario.email,
            valor=email
        )
