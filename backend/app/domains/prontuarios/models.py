from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.connection import Base


class Prontuario(Base):
    """ Classe de Prontuarios """
    __tablename__ = 'prontuarios'

    prontuario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    consulta = Column(Integer, ForeignKey('consultas.consulta_id', ondelete="CASCADE"), nullable=False)
    exame_clinico = Column(Integer, ForeignKey('exames_clinicos.exame_id', ondelete="CASCADE"), nullable=False)
    exame_imagem = Column(Integer, ForeignKey('exames_imagem.exame_id', ondelete="CASCADE"), nullable=False)
    medicamento = Column(Integer, ForeignKey('medicamentos.medicamento_id', ondelete="CASCADE"), nullable=False)

    doenca_prontuarios = relationship("DoencaProntuario", back_populates="prontuario")
    habitos_vida = relationship("HabitosVida", back_populates="prontuario", uselist=False)
    historico = relationship("Historico", back_populates="prontuario", uselist=False)
    # upload_prontuario = relationship("UploadProntuario", back_populates="prontuario", uselist=False)


class Historico(Base):
    """ Classe base de historico de dados dos habitos de vida """
    __tablename__ = 'historicos'

    historico_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    modificacao = Column(String(45), nullable=False)
    data_modificacao = Column(String(20), nullable=False)
    prontuario_id = Column(Integer, ForeignKey('prontuarios.prontuario_id'), nullable=False)

    prontuario = relationship("Prontuario", back_populates="historico")