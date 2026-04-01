from pydantic import BaseModel
from typing import Optional

from app.domains.medicamentos.schemas import MedicamentosPublic


class UploadExameImagemBase(BaseModel):
    """ Classe base"""

    titulo: str
    caminho_upload: str

    exame_imagem_id: int


class UploadExameImagemPublic(BaseModel):
    """ Classe publica """

    upload_id: int

    titulo: str
    caminho_upload: str

    exame_imagem_id: int

    class Config:
        from_attributes = True


class UploadExameImagemCreate(UploadExameImagemBase):
    pass


class ExameImagemBase(BaseModel):
    """ Classe base de Imagens """

    tipo: str
    descricao: str
    link_imagem: str


class ExameImagemPublic(BaseModel):
    """ Classe publica """

    exame_id: int
    tipo: str
    descricao: str
    link_imagem: str

    medicamento: MedicamentosPublic
    upload_imagem: UploadExameImagemPublic

    class Config:
        from_attributes = True


class ExameImagemCreate(ExameImagemBase):
    pass

