from pydantic import BaseModel
from typing import Optional

from app.domains.medicamentos.schemas import MedicamentosPublic


class UploadExameImagemBase(BaseModel):
    """Classe base"""

    titulo: str
    caminho_upload: str

    exame_imagem_id: int


class UploadExameImagemPublic(BaseModel):
    """Classe publica"""

    upload_id: int

    titulo: str
    caminho_upload: str

    exame_imagem_id: int

    class Config:
        from_attributes = True


class UploadExameImagemCreate(UploadExameImagemBase):
    pass


class ExameImagemBase(BaseModel):
    """Classe base de Imagens"""

    tipo: str
    descricao: str
    link_imagem: str


class ExameImagemPublic(BaseModel):
    """Classe publica"""

    exame_id: int
    task_id: str | None = None
    paciente_id: int | None = None
    tipo: str
    descricao: str | None = None
    link_imagem: str | None = None

    medicamento: list[MedicamentosPublic] = []
    upload_imagem: list[UploadExameImagemPublic] = []

    class Config:
        from_attributes = True


class ExameImagemCreate(ExameImagemBase):
    pass


class ExameComUploadResponse(BaseModel):
    exame: ExameImagemPublic
    upload: UploadExameImagemPublic
