from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# from app.database.connection import Base


class Medico(Base):
    """ Model de Médicos"""

    __tablename__ = "medicos"

    medico_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    cpf = Column(String(14), nullable=False, unique=True)
    rg = Column(String(45), nullable=False)
    crm_numero = Column(String(45), nullable=False, unique=True)
    crm_UF = Column(String(45), nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.usuario_id"), nullable=False)
    area_id = Column(Integer, ForeignKey("areas.area_id"), nullable=False)

    usuario = relationship("Usuario", back_populates="medicos")    # criando uma relação bidirecional que permite acessar o usuario de um médico e todos os médicos de um usuario
    area = relationship("Area", back_populates="medicos")          # relação para que médico possua uma área
    consultas = relationship("Consulta", back_populates="medico")  # relação para que um médico peça uma consulta

