from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.connection import Base


class Secretaria(Base):
    """ Model Secretária"""

    __tablename__ = "secretarias"

    secretaria_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cpf = Column(String(14), nullable=False, unique=True)
    rg = Column(String(15), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id", ondelete="CASCADE"), nullable=False)  # ForeignKey de usuario

    usuario = relationship("Usuario", back_populates="secretarias")  # criando uma relação bidirecional que permite acessar o usuario de uma secretaria e todas as secretarias de um usuario
    consultas = relationship("Consulta", back_populates="secretaria")  # relação para que secretárias agendem consultas

