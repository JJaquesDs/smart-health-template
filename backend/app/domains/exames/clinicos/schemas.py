from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.domains.medicamentos.schemas import MedicamentosPublic


class ExamesClinicosBase(BaseModel):
    """Classe base de exames clinicos """

    ist: bool
    ist_numero: int
    ist_hiv: bool
    ist_diagnosticadas_num: int

    diagnostico_cancer: bool
    diagnostico_cin: bool
    diagnostico_hpv: bool
    diagnostico: bool

    hinselmann: bool
    schiller: bool
    citologia: bool
    biopsia: bool


class ExameClinicoPublic(BaseModel):
    """ Classe publica de exame clinico"""

    exame_id: int

    ist: bool
    ist_numero: int
    ist_hiv: bool
    ist_diagnosticadas_num: int

    diagnostico_cancer: bool
    diagnostico_cin: bool
    diagnostico_hpv: bool
    diagnostico: bool

    hinselmann: bool
    schiller: bool
    citologia: bool
    biopsia: bool

    medicamento: MedicamentosPublic  # verificar depois duvidas


class ExamesClinicoCreate(ExamesClinicosBase):
    pass


class ExamesClinicoUpdate(BaseModel):
    """ Classe para atualizar exames clinicos """

    ist: Optional[bool]
    ist_numero: Optional[int]
    ist_hiv: Optional[bool]
    ist_diagnosticadas_num: Optional[int]

    diagnostico_cancer: Optional[bool]
    diagnostico_cin: Optional[bool]
    diagnostico_hpv: Optional[bool]
    diagnostico: Optional[bool]

    hinselmann: Optional[bool]
    schiller: Optional[bool]
    citologia: Optional[bool]
    biopsia: Optional[bool]


class ExamesClinicosGet(BaseModel):
    exame_id: int

    ist: bool
    ist_numero: int
    ist_hiv: bool
    ist_diagnosticadas_num: int

    diagnostico_cancer: bool
    diagnostico_cin: bool
    diagnostico_hpv: bool
    diagnostico: bool

    hinselmann: bool
    schiller: bool
    citologia: bool
    biopsia: bool

    class Config:
        from_attributes = True


ExameCategoria = Literal["laboratorial", "imagem", "funcional", "outros"]


class ExameCatalogoBase(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    categoria: ExameCategoria
    descricao: str = Field(min_length=1)
    preco: Decimal = Field(ge=0)
    preparacao: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: bool = True


class ExameCatalogoCreate(ExameCatalogoBase):
    pass


class ExameCatalogoUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=1, max_length=120)
    categoria: Optional[ExameCategoria] = None
    descricao: Optional[str] = Field(default=None, min_length=1)
    preco: Optional[Decimal] = Field(default=None, ge=0)
    preparacao: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: Optional[bool] = None


class ExameCatalogoPublic(ExameCatalogoBase):
    model_config = ConfigDict(from_attributes=True)

    exame_id: int

