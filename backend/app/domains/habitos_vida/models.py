from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.core.connection import Base


class HabitosVida(Base):
    """ Classe base para habitos de vida """
    __tablename__ = 'habitos_vida'

    habitos_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    numero_parceiros = Column(Integer, nullable=True)
    primeira_relacao = Column(Integer, nullable=True)
    numero_gravidez = Column(Integer, nullable=True)

    fuma = Column(Boolean, nullable=True)
    fuma_anos = Column(Integer, nullable=True)

    contraceptivo_hormonal = Column(Boolean, nullable=True)
    contraceptivo_hormonal_anos = Column(Integer, nullable=True)

    diu = Column(Boolean, nullable=True)
    diu_anos = Column(Integer, nullable=True)

    prontuario_id = Column(Integer, ForeignKey('prontuarios.prontuario_id', ondelete="CASCADE"), nullable=False)

    prontuario = relationship("Prontuario", back_populates="habitos_vida")


class ResultadoAnaliseHabito(Base):
    __tablename__ = "resultado_analise_habito"

    resultado_analise_hb_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    risco = Column(Float, nullable=False)   # Pode mudar
    observacoes = Column(String, nullable=True)
    habito_id = Column(Integer, ForeignKey('habitos_vida.habitos_id'))
