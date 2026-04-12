from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


from app.domains.professionals.medico.medico_esp.enums_med_esp import StatusEsp

from app.core.connection import Base


class MedicoEspecialidade(Base):
    """ Model para guardar relacionamento de 'Especialidades'|'Médicos' (N*N)"""

    __tablename__ = "medico_especialidades"

    med_esp_id = Column(type_=Integer, primary_key=True, index=True, autoincrement=True)

    medico_id = Column(Integer, ForeignKey(column="medicos.medico_id", ondelete="CASCADE"), nullable=False)
    esp_id = Column(Integer, ForeignKey(column="especialidades.esp_id", ondelete="CASCADE"), nullable=False)

    # Enum de status
    status = Column(Enum(StatusEsp))

    # Relacionamentos sqlalchemy
    medico = relationship(argument="Medico", back_populates="med_esps")
    especialidade = relationship(argument="Especialidade", back_populates="medicos")



