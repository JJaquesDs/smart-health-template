from pydantic import BaseModel

from app.domains.professionals.medico.medico_esp.enums_med_esp import StatusEsp

from app.domains.professionals.medico.especialidade.esp_schemas import (
    EspecialidadeResumo,
)


class MedicoEspBase(BaseModel):
    """ Classe base de 'Especialidade do Médico' """

    status: StatusEsp


class MedicoEspPublic(BaseModel):
    """ CLasse Públic de 'Especialidade do Médico' """

    med_esp_id: int

    medico: "MedicoResumo"                  ## Evitando erro de import circular
    especialidade: EspecialidadeResumo

    status: StatusEsp

    class Config:
        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class MedicoEspCreate(BaseModel):
    """ Classe para criar 'Medico Especialidade' """

    esp_id: int
    status: StatusEsp


class MedicoEspUpdate(BaseModel):
    """ Classe para Atualizar um 'Medico Especialidae' """

    esp_id: int
    status: StatusEsp


from app.domains.professionals.medico.schemas import MedicoResumo

MedicoEspPublic.model_rebuild()  ## Resolve a classe depois que carregar tudo (erro de import circular)
