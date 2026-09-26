from datetime import datetime, date
from typing import Optional, Literal
import re

from pydantic import BaseModel, EmailStr, field_validator


def normalize_cpf(value: str) -> str:
    if value is None:
        raise ValueError("CPF não pode ser nulo")
    value = value.strip()
    if not re.fullmatch(r"(?:[0-9]{11}|[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2})", value):
        raise ValueError("CPF deve conter 11 dígitos ou usar o formato 000.000.000-00")
    digits = re.sub(r"[^0-9]", "", value)
    if len(set(digits)) == 1:
        raise ValueError("CPF inválido")
    for size in (9, 10):
        check = (sum(int(digits[i]) * (size + 1 - i) for i in range(size)) * 10) % 11
        if int(digits[size]) != (0 if check == 10 else check):
            raise ValueError("CPF inválido: confira os dígitos verificadores")
    return digits


PATIENT_LIMITS = {
    "nome": 255, "cpf": 45, "data_nascimento": 10, "genero": 45,
    "email": 45, "telefone": 45, "rua": 255, "numero": 45,
    "complemento": 255, "cidade": 120, "estado": 45, "cep": 20,
    "tipo_sanguineo": 10, "ultimo_exame": 255,
    "contato_emergencia_nome": 255, "contato_emergencia_parentesco": 120,
    "contato_emergencia_telefone": 45,
}
REQUIRED_PATIENT_FIELDS = {"nome", "cpf", "data_nascimento", "genero", "email", "telefone"}


class PatientInputValidation(BaseModel):
    @field_validator("*", mode="before")
    @classmethod
    def validate_patient_field(cls, value, info):
        name = info.field_name
        if isinstance(value, str):
            value = value.strip()
        if name in REQUIRED_PATIENT_FIELDS and (value is None or value == ""):
            raise ValueError(f"{name}: campo obrigatório")
        limit = PATIENT_LIMITS.get(name)
        if limit and isinstance(value, str) and len(value) > limit:
            raise ValueError(f"{name}: máximo de {limit} caracteres")
        if name == "data_nascimento":
            try:
                if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
                    raise ValueError()
                birthday = date.fromisoformat(value)
            except ValueError:
                raise ValueError("Data de nascimento inválida; use AAAA-MM-DD")
            if birthday > date.today():
                raise ValueError("Data de nascimento não pode estar no futuro")
        return value


class PacienteBase(BaseModel):
    nome: str
    cpf: str
    data_nascimento: str
    genero: str
    email: EmailStr
    telefone: str
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    dados_clinicos: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    ultimo_exame: Optional[str] = None
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    historico_medico: Optional[str] = None
    observacoes: Optional[str] = None
    contato_emergencia_nome: Optional[str] = None
    contato_emergencia_parentesco: Optional[str] = None
    contato_emergencia_telefone: Optional[str] = None


class PacienteCreate(PacienteBase, PatientInputValidation):
    _validate_cpf = field_validator("cpf")(normalize_cpf)


class PacienteUpdate(PatientInputValidation):
    _validate_cpf = field_validator("cpf")(normalize_cpf)
    status: Literal["active", "inactive"] = "active"
    nome: Optional[str] = None
    cpf: Optional[str] = None
    data_nascimento: Optional[str] = None
    genero: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    dados_clinicos: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    ultimo_exame: Optional[str] = None
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    historico_medico: Optional[str] = None
    observacoes: Optional[str] = None
    contato_emergencia_nome: Optional[str] = None
    contato_emergencia_parentesco: Optional[str] = None
    contato_emergencia_telefone: Optional[str] = None

    class Config:
        from_attributes = True


class PacientePublic(BaseModel):
    created_at: datetime | None
    updated_at: datetime | None
    status: Literal["active", "inactive"]
    paciente_id: int
    nome: str
    cpf: str
    data_nascimento: str
    genero: str
    email: EmailStr
    telefone: str
    rua: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    dados_clinicos: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    ultimo_exame: Optional[str] = None
    alergias: Optional[str] = None
    medicamentos: Optional[str] = None
    historico_medico: Optional[str] = None
    observacoes: Optional[str] = None
    contato_emergencia_nome: Optional[str] = None
    contato_emergencia_parentesco: Optional[str] = None
    contato_emergencia_telefone: Optional[str] = None

    class Config:
        from_attributes = True


class PacientPublic(PacientePublic):
    pass


class PacientOut(PacientePublic):
    pass


class PacientUpdate(PacienteUpdate):
    pass


class PacienteHistoricoClinicoBase(BaseModel):
    titulo: str
    descricao: str
    data_registro: str


class PacienteHistoricoClinicoCreate(PacienteHistoricoClinicoBase):
    pass


class PacienteHistoricoClinicoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_registro: Optional[str] = None

    class Config:
        from_attributes = True


class PacienteHistoricoClinicoPublic(PacienteHistoricoClinicoBase):
    historico_id: int
    paciente_id: int

    class Config:
        from_attributes = True


class PacienteExameBase(BaseModel):
    nome: str
    data_exame: str
    status: str
    resultado: str
    descricao: Optional[str] = None
    observacoes: Optional[str] = None
    pdf_nome: Optional[str] = None
    pdf_url: Optional[str] = None


class PacienteExameCreate(PacienteExameBase):
    pass


class PacienteExameUpdate(BaseModel):
    nome: Optional[str] = None
    data_exame: Optional[str] = None
    status: Optional[str] = None
    resultado: Optional[str] = None
    descricao: Optional[str] = None
    observacoes: Optional[str] = None
    pdf_nome: Optional[str] = None
    pdf_url: Optional[str] = None

    class Config:
        from_attributes = True


class PacienteExamePublic(PacienteExameBase):
    paciente_exame_id: int
    paciente_id: int

    class Config:
        from_attributes = True


class PacienteMedicamentoBase(BaseModel):
    nome: str
    dosagem: Optional[str] = None
    periodo: str
    status: str
    descricao: str
    observacoes: Optional[str] = None


class PacienteMedicamentoCreate(PacienteMedicamentoBase):
    pass


class PacienteMedicamentoUpdate(BaseModel):
    nome: Optional[str] = None
    dosagem: Optional[str] = None
    periodo: Optional[str] = None
    status: Optional[str] = None
    descricao: Optional[str] = None
    observacoes: Optional[str] = None

    class Config:
        from_attributes = True


class PacienteMedicamentoPublic(PacienteMedicamentoBase):
    paciente_medicamento_id: int
    paciente_id: int

    class Config:
        from_attributes = True
