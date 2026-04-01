from pydantic import BaseModel
from typing import Optional


class DoencaBase(BaseModel):
    """ Classe base de doencas """

    nome: str
    status: str


class DoencaCreate(DoencaBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’ / 'Get') """
    pass


class DoencaPublic(BaseModel):
    """ Classe public para retornar dados na api """

    doenca_id: int

    nome: str
    status: str

    class Config:
        from_attributes = True


class DoencaUpdate(BaseModel):
    """ Classe para atualizar doencas """

    nome: Optional[str]
    status: Optional[str]


class DoencaGet(BaseModel):
    doenca_id: int
    nome: str
    status: str

    class Config:
        from_attributes = True
