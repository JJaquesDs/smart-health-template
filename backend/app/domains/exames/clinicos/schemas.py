from pydantic import BaseModel
from typing import Optional

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

