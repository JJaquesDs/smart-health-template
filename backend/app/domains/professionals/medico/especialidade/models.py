from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.connection import Base


class Especialidade(Base):
    __tablename__ = "especialidades"

    esp_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(45), nullable=False, unique=True)

    medicos = relationship(                 # relação 'N:N' via tabela associativa 'MedicoEspecialidade'
        argument="MedicoEspecialidade",
        back_populates="especialidade"
    )
