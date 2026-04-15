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
