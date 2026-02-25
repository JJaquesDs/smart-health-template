from pydantic import BaseModel
from typing import Optional

from app.users.schemas import UserPublic
from area.schemas import AreaPublic


class MedicoBase(BaseModel):
    """ Classe base de Medicos """

    nome: str
    cpf: str
    rg: str
    crm_numero: str
    crm_UF: str
    usuario_id: int
    area_id: int


class MedicoPublic(BaseModel):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """

    medico_id: int
    nome: str
    cpf: str
    rg: str
    crm_numero: str
    crm_UF: str
    usuario: UserPublic
    area: AreaPublic

    class Config:
        orm_mode = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class MedicoCreate(MedicoBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’ / 'Get') """
    pass


class MedicoUpdate(BaseModel):
    """ Classe de atualização de médicos"""

    nome: Optional[str]
    area_id: Optional[int]


class MedicoGet(BaseModel):
    """ Classe para retornar dados de médicos """

    medico_id: int
    nome: str
    cpf: str
    rg: str
    crm_numero: str
    crm_UF: str
    usuario_id: int
    area_id: int

    class Config:
        orm_mode = True
