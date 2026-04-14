from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.connection import Base


class ExamesClinicos(Base):
    """ Tabela base de exames clínicos"""

    __tablename__ = 'exames_clinicos'

    exame_id = Column(Integer, primary_key=True, autoincrement=True)

    ist = Column(Boolean, nullable=True)
    ist_numero = Column(Integer, nullable=True)
    ist_hiv = Column(Boolean, nullable=True)
    ist_diagnosticadas_num = Column(Integer, nullable=True)

    diagnostico_cancer = Column(Boolean, nullable=True)
    diagnostico_cin = Column(Boolean, nullable=True)
    diagnostico_hpv = Column(Boolean, nullable=True)
    diagnostico = Column(Boolean, nullable=True)

    hinselmann = Column(Boolean, nullable=True)
    schiller = Column(Boolean, nullable=True)
    citologia = Column(Boolean, nullable=True)
    biopsia = Column(Boolean, nullable=True)

    medicamento = relationship("Medicamento", back_populates="exame_clinico")   # Para Medicamentos se relacionarem a exames


class ResultadoExameClinicoIa:
    """ Tabela para persistir resultados de análise de exames clínicos pelo modelo """

    __tablename__ = 'resultados_analise_exame_clinico_ia'

    predicao_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    risco = Column(String(10), nullable=False)
    data_analise = Column(DateTime, default=datetime.utcnow())

    exame_clinico_id = Column(Integer, ForeignKey('exames_clinicos.exame_id'))              #  Relacionando o resultado da analise clinica com o exame clinico atraves de ForeignKey
    exame_clinico = relationship("ExamesClinicos", back_populates="resultados")


    #  Ela ainda n tem schemas ou classe pública, pois não possui dados sensíveis como senhas


class ExameCatalogo(Base):
    """Catálogo de exames usado pelo frontend administrativo."""

    __tablename__ = "catalogo_exames"

    exame_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(120), nullable=False, unique=True)
    categoria = Column(String(30), nullable=False)
    descricao = Column(Text, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    preparacao = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)

