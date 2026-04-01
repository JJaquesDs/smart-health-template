from pydantic import BaseModel
from typing import Optional


class ProntuarioBase(BaseModel):
    """ Classe base de prontuario"""

    consulta: int
    exame_clinico: int
    exame_imagem: int
    medicamento: int


class ProntuarioCreate(ProntuarioBase):
    pass


class ProntuarioPublic(BaseModel):
    """ Classe Publica de prontuario """

    prontuario_id: int

    class Config:
        from_atributes = True


# -- Schemas de historico -- #
class HistoricoBase(BaseModel):
    """ Classe base de historico do paciente """

    modificacao: str
    data_modificacao: str

    prontuario_id: int


class HistoricoPublic(BaseModel):
    """ Classe Publica de Historico para transferencia de dados na api"""
    historico_id: int
    modificacao: str
    data_modificacao: str

    prontuario: ProntuarioPublic


class HistoricoCreate(HistoricoBase):
    pass


class HistoricoUpdate(BaseModel):
    """ Classe para atualizar historico """

    modificacao: Optional[str]
    data_modificacao: Optional[str]


class HistoricoGet(BaseModel):
    """ Classe para retornar dados de prontuarios """
    historico_id: int
    modificacao: str
    data_modificacao: str

    class Config:
        from_attributes = True
