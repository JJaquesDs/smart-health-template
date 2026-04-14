from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.domains.users.enums import UserRole

from app.core.connection import Base


class Usuario(Base):
    """ Model de Usuários"""

    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(45), unique=True, nullable=False)
    senha = Column(String(80), nullable=False)
    nome = Column(String(45), nullable=False)
    telefone = Column(String(45), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)   ## Role padrão é "user"
    registro_profissional = Column(String(60), nullable=True)
    especialidade_principal = Column(String(120), nullable=True)
    instituicao = Column(String(120), nullable=True)
    universidade = Column(String(120), nullable=True)
    ano_formacao = Column(Integer, nullable=True)
    residencia_medica = Column(String(120), nullable=True)
    especializacoes = Column(JSON, nullable=True)

    # Relacionamentos
    medicos = relationship("Medico", back_populates="usuario")
    secretarias = relationship("Secretaria", back_populates="usuario")
    admins = relationship("Administrador", back_populates="usuario")


class Administrador(Base):
    """ Model Adminstrador"""
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(45), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id", ondelete="CASCADE"), nullable=False)
    usuario = relationship("Usuario", back_populates="admins")

