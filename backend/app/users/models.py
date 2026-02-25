from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# from app.database.connection import Base


class Usuario(Base):
    """ Model de Usuários"""

    __tablename__ = "usuarios"

    usuario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(45), unique=True, nullable=False)
    senha = Column(String(80), nullable=False)
    nome = Column(String(45), nullable=False)
    telefone = Column(String(45), nullable=False)

    # Relacionamentos
    medicos = relationship("Medico", back_populates="usuario")
    secretarias = relationship("Secretaria", back_populates="usuario")
    admins = relationship("Administrador", back_populates="usuario")


class Administrador(Base):
    """ Model Adminstrador"""
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(45), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    usuario = relationship("Usuario", back_populates="admins")

