from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.connection import Base


class Consulta(Base):
    """ Model de Consultas """

    __tablename__ = 'consultas'

    consulta_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    data_consulta = Column(String(10), nullable=False)

    medico_id = Column(Integer, ForeignKey('medicos.medico_id', ondelete="CASCADE"), nullable=False)
    secretaria_id = Column(Integer, ForeignKey('secretarias.secretaria_id', ondelete="CASCADE"), nullable=False)
    paciente_id = Column(Integer, ForeignKey('pacientes.paciente_id', ondelete="CASCADE"), nullable=False)

    # RELACIONAMENTOS
    medico = relationship("Medico", back_populates="consultas")
    secretaria = relationship("Secretaria", back_populates="consultas")
    paciente = relationship("Paciente", back_populates="consultas")
