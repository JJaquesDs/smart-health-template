from sqlalchemy.orm import Session

from app.domains.professionals.medico.medico_esp.model import MedicoEspecialidade


def create_med_esp_db(session: Session, med_esp: MedicoEspecialidade):
    """ Função para salvar no banco de dados 'Medico Especialidade' """

    session.add(med_esp)
    session.flush()

    return med_esp
