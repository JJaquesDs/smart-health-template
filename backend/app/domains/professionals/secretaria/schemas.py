from pydantic import BaseModel
from typing import Optional

from app.domains.users.schemas import UserCreate, UserPublic

from app.domains.users.enums import UserRole


class SecretariaBase(BaseModel):
    """ Modelo Base de secretária """
    cpf: str
    rg: str


class SecretariaCreate(SecretariaBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’ / 'Get') """

    cpf: str
    rg: str
    user: UserCreate


class SecretariaPublic(BaseModel):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """
    secretaria_id: int
    cpf: str
    rg: str
    usuario: UserPublic

    class Config:
        """ Classe de configuração do modelo publico, para mais atributos consultar a documentação"""

        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class SecretariaUpdate(BaseModel):
    """ Classe para atualizar Secretaria """

    cpf: Optional[str]
    rg: Optional[str]


class SecretariaGet(BaseModel):
    """ Classe para buscar dados de Secretaria """

    secretaria_id: int
    cpf: str
    rg: str
    usuario_id: int

    class Config:
        from_attributes = True
