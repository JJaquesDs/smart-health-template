from pydantic import BaseModel
from typing import Optional


class AreaBase(BaseModel):
    """ Classe base de Área de atuação """

    titulo: str
    status: str


class AreaPublic(AreaBase):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """
    area_id: int

    class Config:
        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class AreaCreate(AreaBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’) """
    pass


class AreaUpdate(BaseModel):
    """ Classe de atualização de area """
    titulo: Optional[str]
    status: Optional[str]
