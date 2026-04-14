from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.connection import Base


class Medicamento(Base):
    """ Classe Medicamentos """

    __tablename__ = 'medicamentos'

    medicamento_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descricao = Column(String(100))

    exame_clinico_id = Column(Integer, ForeignKey('exames_clinicos.exame_id', ondelete="CASCADE"), nullable=False)
    exame_imagem_id = Column(Integer, ForeignKey('exames_imagem.exame_id', ondelete="CASCADE"), nullable=False)

    # RELACIONAMENTO
    exame_clinico = relationship("ExamesClinicos", back_populates="medicamento")
    exame_imagem = relationship("ExameImagem", back_populates="medicamento")


class MedicamentoCatalogo(Base):
    """Catálogo de medicamentos usado pelo frontend administrativo."""

    __tablename__ = "catalogo_medicamentos"

    medicamento_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(120), nullable=False, unique=True)
    principio_ativo = Column(String(120), nullable=False)
    dosagem = Column(String(60), nullable=False)
    forma_farmaceutica = Column(String(30), nullable=False)
    fabricante = Column(String(120), nullable=False)
    descricao = Column(Text, nullable=True)
    contraindicacoes = Column(Text, nullable=True)
    efeitos_colaterais = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
