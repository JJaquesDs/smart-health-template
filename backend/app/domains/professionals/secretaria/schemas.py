from pydantic import BaseModel
from typing import Optional

from app.domains.users.schemas import UserPublic


class SecretariaBase(BaseModel):
    """ Modelo Base de secretária """
    nome: str
    cpf: str
    rg: str
    usuario_id: int


class SecretariaCreate(SecretariaBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’ / 'Get') """
    pass


class SecretariaPublic(BaseModel):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """
    secretaria_id: int
    nome: str
    cpf: str
    rg: str
    usuario: UserPublic

    class Config:
        """ Classe de configuração do modelo publico, para mais atributos consultar a documentação"""

        orm_mode = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class SecretariaUpdate(BaseModel):
    """ Classe para atualizar Secretaria """

    nome: Optional[str]


class SecretariaGet(BaseModel):
    """ Classe para buscar dados de Secretaria """

    secretaria_id: int
    nome: str
    cpf: str
    rg: str
    usuario_id: int

    class Config:
        orm_mode = True
