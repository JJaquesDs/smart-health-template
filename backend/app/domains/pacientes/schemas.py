from typing import Optional

from pydantic import BaseModel, EmailStr


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


class PacienteCreate(PacienteBase):
    pass


class PacienteUpdate(BaseModel):
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
