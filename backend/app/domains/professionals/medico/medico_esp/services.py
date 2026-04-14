from fastapi import HTTPException


from sqlalchemy.orm import Session

from app.domains.professionals.medico.models import Medico

from app.domains.professionals.medico.medico_esp.model import MedicoEspecialidade

from app.domains.professionals.medico.especialidade.repository import get_esp_by_id

from app.domains.professionals.medico.medico_esp.schemas import MedicoEspUpdate

from app.domains.professionals.medico.medico_esp.repository import (
    create_med_esp_db
)


def update_medico_esp_service(
        session: Session,
        medico: Medico,
        med_esps: list[MedicoEspUpdate]
):
    """ Service para atualizar 'Medico Especialidade' """

    atuais = {
        relacionamento.esp_id: relacionamento for relacionamento in medico.med_esps
    }

    novos = {
        esp.esp_id: esp for esp in med_esps
    }

    # Atualizar ou criar uma
    for esp_id, esps in novos.items():

        especialidade = get_esp_by_id(session=session, esp_id=esp_id)

        if not especialidade:
            raise HTTPException(
                status_code=404,
                detail=f"Especialidade {esp_id} não encontrada"
            )

        # Atualizando 'status'
        if esp_id in atuais:
            atuais[esp_id].status = esps.status

        else:
            # Se não houver cria relação
            nova = MedicoEspecialidade(
                medico_id=medico.medico_id,
                esp_id=esp_id,
                status=esps.status
            )

            create_med_esp_db(session=session, med_esp=nova)

    # deletar o que não veio mais
    for esp_id, relacionamento in atuais.items():
        if esp_id not in novos:
            session.delete(relacionamento)
