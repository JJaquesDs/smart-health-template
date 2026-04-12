from pydantic import BaseModel
from typing import Optional


class EspecialidadeBase(BaseModel):
    """ Classe base de Área de atuação """

    titulo: str


class EspecialidadePublic(EspecialidadeBase):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """
    esp_id: int

    class Config:
        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class EspecialidadeResumo(BaseModel):
    """ 'Especialidade Resumo' irá evitar loops infinitos e 'jsons' gigantes """

    esp_id: int
    titulo: str

    class Config:
        from_attributes = True


class EspecialidadeCreate(EspecialidadeBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’) """
    pass


class EspecialidadeUpdate(BaseModel):
    """ Classe de atualização de especialidade """
    titulo: Optional[str]
