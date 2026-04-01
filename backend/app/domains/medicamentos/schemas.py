from pydantic import BaseModel
from typing import Optional


class MedicamentosBase(BaseModel):
    """ Classe base de medicamentos """

    descricao: str

    exame_clinico_id: int
    exame_imagem_id: int


class MedicamentosPublic(BaseModel):
    medicamento_id: int

    descricao: str

    exame_clinico_id: int
    exame_imagem_id: int

    class Config:
        from_attributes = True


class MedicamentoCrate(MedicamentosBase):
    pass


class MedicamentosUpdate(BaseModel):
    descricao: Optional[str]


class MedicamentosGet(BaseModel):
    medicamento_id: int

    descricao: str

    exame_clinico_id: int
    exame_imagem_id: int

    class Config:
        from_attributes = True

