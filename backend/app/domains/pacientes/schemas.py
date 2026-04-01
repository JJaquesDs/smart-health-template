from pydantic import BaseModel, EmailStr
from typing import Optional


class PacienteBase(BaseModel):
    """ Classe base Paciente """

    nome: str
    data_nascimento: str
    rg: str
    cpf: str
    data_cadastro: str
    endereco: str
    telefone: str
    email: EmailStr
    plano_saude: bool


class PacientPublic(BaseModel):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """

    paciente_id: int
    nome: str
    data_nascimento: str
    rg: str
    cpf: str
    data_cadastro: str
    endereco: str
    telefone: str
    email: EmailStr
    plano_saude: bool

    class Config:
        from_attributes = True   # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class PacientOut(PacientPublic):
    """ Classe Pacient Out ???? """
    pass


class PacienteCreate(PacienteBase):
    """ Schema nao adiciona nem remove campos ao Modelo Base (serve apenas para separar das demais classes: 'Base' / ‘Update’ / 'Get')"""
    pass


class PacientUpdate(BaseModel):
    """ Classe de atualizalção de pacientes"""

    nome: Optional[str]
    data_nascimento: Optional[str]
    rg: Optional[str]
    cpf: Optional[str]
    data_cadastro: Optional[str]
    endereco: Optional[str]
    telefone: Optional[str]
    email: Optional[EmailStr]
    plano_saude: Optional[bool]

    class Config:
        from_attributes = True
