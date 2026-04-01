from pydantic import BaseModel
from typing import Optional

from app.domains.professionals.medico.schemas import MedicoPublic
from app.domains.professionals.secretaria.schemas import SecretariaPublic
from app.domains.pacientes.schemas import PacientPublic


class ConsultaBase(BaseModel):
    """ Classe base de Consultas """

    data_consulta: str

    medico_id: int
    secretaria_id: int
    paciente_id: int


class ConsultaPublic(BaseModel):
    """ Classe Publica de consulta para retornar dados pela api """

    consulta_id: int
    data_consulta: str

    medico: MedicoPublic
    secretaria: SecretariaPublic
    paciente: PacientPublic

    class Config:
        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class ConsultaCreate(ConsultaBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’ / 'Get') """
    pass


class ConsultaUpdate(BaseModel):
    """ Classe para atualizar consultas"""

    data_consulta: Optional[str]
    medico_id: Optional[int]   # Caso precise mudar de médico


class ConsultaGet(BaseModel):
    """ Classe para retornar dados de consultas """

    consulta_id: int
    data_consulta: str

    medico_id: int
    secretaria_id: int
    paciente_id: int

    class Config:
        from_attributes = True

