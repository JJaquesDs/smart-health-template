from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


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


FormaFarmaceutica = Literal[
    "comprimido",
    "capsula",
    "injetavel",
    "liquido",
    "topico",
    "outros",
]


class MedicamentoCatalogoBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    principio_ativo: str = Field(min_length=1, max_length=120)
    dosagem: str = Field(min_length=1, max_length=60)
    forma_farmaceutica: FormaFarmaceutica
    fabricante: str = Field(min_length=1, max_length=120)
    descricao: Optional[str] = None
    contraindicacoes: Optional[str] = None
    efeitos_colaterais: Optional[str] = None
    ativo: bool = True


class MedicamentoCatalogoCreate(MedicamentoCatalogoBase):
    pass


class MedicamentoCatalogoUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=1, max_length=120)
    principio_ativo: Optional[str] = Field(default=None, min_length=1, max_length=120)
    dosagem: Optional[str] = Field(default=None, min_length=1, max_length=60)
    forma_farmaceutica: Optional[FormaFarmaceutica] = None
    fabricante: Optional[str] = Field(default=None, min_length=1, max_length=120)
    descricao: Optional[str] = None
    contraindicacoes: Optional[str] = None
    efeitos_colaterais: Optional[str] = None
    ativo: Optional[bool] = None


class MedicamentoCatalogoPublic(MedicamentoCatalogoBase):
    model_config = ConfigDict(from_attributes=True)

    medicamento_id: int

