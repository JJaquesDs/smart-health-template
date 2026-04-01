from pydantic import BaseModel
from typing import Optional

from app.domains.prontuarios.schemas import ProntuarioPublic


class HabitoVidaBase(BaseModel):
    """ Classe base de habitos de vida """
    numero_parceiros: int
    primeira_relacao: int
    numero_gravidez: int

    fuma: bool
    fuma_anos: int

    contraceptivo_hormonal: bool
    contraceptivo_hormonal_anos: int

    diu: bool
    diu_anos: int

    prontuario_id: int


class ResultAnaliseHabitosBase(BaseModel):
    """ Classse base para resultados de analises de habitos de vida """

    risco: float
    observacoes: Optional[int]

    habito_id: int


# --- shemas de habitos de vida --- #


class HabitoVidaPublic(BaseModel):
    """ Classe Públic de Habito de Vida """
    habitos_id: int

    numero_parceiros: int
    primeira_relacao: int
    numero_gravidez: int

    fuma: bool
    fuma_anos: int

    contraceptivo_hormonal: bool
    contraceptivo_hormonal_anos: int

    diu: bool
    diu_anos: int

    prontuario_id: ProntuarioPublic

    class Config:
        from_attributes = True  ## Mudou


class HabitoVidaCreate(HabitoVidaBase):
    pass


class HabitoVidaUpdate(BaseModel):
    """ Classe para atualizar habitos de vida """
    numero_parceiros: Optional[int]
    primeira_relacao: Optional[int]
    numero_gravidez: Optional[int]

    fuma: Optional[bool]
    fuma_anos: Optional[int]

    contraceptivo_hormonal: Optional[bool]
    contraceptivo_hormonal_anos: Optional[int]

    diu: Optional[bool]
    diu_anos: Optional[int]


class HabitosVidaGet(BaseModel):
    numero_parceiros: Optional[int]
    primeira_relacao: Optional[int]
    numero_gravidez: Optional[int]

    fuma: Optional[bool]
    fuma_anos: Optional[int]

    contraceptivo_hormonal: Optional[bool]
    contraceptivo_hormonal_anos: Optional[int]

    diu: Optional[bool]
    diu_anos: Optional[int]

    class Config:
        from_attributes = True

#  -------------------------------  #


# — - Schemmas de resultado de análise de habitos de vida -- #

class ResultAnaliseHabitoBase(BaseModel):
    """ Classe base de resultados de analises de habitos de vida """

    risco: float
    observacoes: str
    habito_id: int


class ResultAnaliseHabitoPublic(BaseModel):
    """ Classe publica """

    resultado_analise_hb_id: int

    risco: float
    observacoes: str

    habito_id: HabitoVidaPublic

    class Config:
        from_attributes = True


class ResultAnaliseHabitoCreate(ResultAnaliseHabitoBase):
    pass


class ResultAnaliseHabitoGet(BaseModel):
    """ Classe para retornar resultados"""
    risco: Optional[float]
    observacoes: Optional[str]
    habito_id: Optional[int]

    class Config:
        from_attributes = True

