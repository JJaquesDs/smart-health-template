from pydantic import BaseModel
from typing import Optional

from app.domains.users.schemas import UserPublic, UserCreate


class MedicoBase(BaseModel):
    """ Classe base de Medicos """

    cpf: str
    rg: str
    crm_numero: str
    crm_UF: str


class MedicoPublic(BaseModel):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """

    medico_id: int
    cpf: str
    rg: str
    crm_numero: str
    crm_UF: str
    usuario: UserPublic

    med_esps: list["MedicoEspPublic"]  ## String para evitar erro de import circular

    class Config:
        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class MedicoResumo(BaseModel):
    """ 'Medico Resumo' irá evitar loops infinitos e 'jsons' gigantes """

    medico_id: int

    class Config:
        from_attributes = True


class MedicoCreate(MedicoBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’ / 'Get') """

    cpf: str
    rg: str
    crm_numero: str
    crm_UF: str
    user: UserCreate

    # Relações com 'Especialidade
    med_esps: list["MedicoEspCreate"]  ## String para evitar erro de import circular


class MedicoUpdate(BaseModel):
    """ Classe de atualização de médicos"""

    cpf: Optional[str]
    rg: Optional[str]
    crm_numero: Optional[str]
    crm_UF: Optional[str]
    med_esp: Optional[list["MedicoEspUpdate"]]


class MedicoGet(BaseModel):
    """ Classe para retornar dados de médicos """

    medico_id: int
    cpf: str
    rg: str
    crm_numero: str
    crm_UF: str
    usuario_id: int
    medd_esp_id: int

    class Config:
        from_attributes = True


from app.domains.professionals.medico.medico_esp.schemas import (
    MedicoEspPublic,
    MedicoEspCreate,
    MedicoEspUpdate
)

MedicoPublic.model_rebuild()  ## Carrega tudo após resolver a classe (erro de import circular)
