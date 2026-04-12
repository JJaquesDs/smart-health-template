from sqlalchemy.orm import Session

from app.domains.professionals.medico.especialidade.models import Especialidade


def create_esp_db(session: Session, especialidade: Especialidade):
    """ Função que cria uma área para um médico """

    session.add(especialidade)

    # garantindo o 'id-autoincrement' do banco de dados
    session.flush()

    return especialidade


def get_esp_db(session: Session, titulo: str) -> Especialidade | None:
    """ Função que retornará se já há essa especialidade no banco de dados"""

    especialidade = session.query(Especialidade).filter_by(titulo=titulo).first()

    return especialidade


def get_esp_by_id(session: Session, esp_id: int) -> Especialidade | None:
    """ Função que retorna se há uma 'Especialidade' pelo 'id' """

    especialidade = session.get(Especialidade, esp_id)

    return especialidade


def get_all_esp_in_db(session: Session) -> list[Especialidade]:  # Retorna uma lista de Usuario
    """ Função que retorna todos os Usuarios"""

    return session.query(Especialidade).all()
