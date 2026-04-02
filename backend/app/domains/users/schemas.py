from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    """ Classe base de usuarios """
    email: EmailStr
    senha: str
    nome: str
    telefone: str
    role: str


class UserPublic(BaseModel):
    """ Classe Pública usada para retornar dados pela API sem expor informações sensiveis """

    usuario_id: int
    nome: str
    telefone: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # Serialização dos dados, dizendo que virão de um orm SQLAlchemy


class UserCreate(BaseModel):
    """ Schema para criacao de novo usuario"""
    email: EmailStr
    senha: str
    nome: str
    telefone: str
    role: str


class UserUpdate(BaseModel):
    """ Classe de atualização de usuarios """

    nome: Optional[str]
    telefone: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]

