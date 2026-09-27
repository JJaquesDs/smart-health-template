from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.connection import Base


class ExameImagem(Base):
    """Tabela Base de Exames"""

    __tablename__ = "exames_imagem"

    exame_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(45), nullable=False)
    descricao = Column(Text)
    link_imagem = Column(String(255))
    task_id = Column(String(36), nullable=True, unique=True, index=True)
    usuario_id = Column(
        Integer, ForeignKey("usuarios.usuario_id", ondelete="SET NULL"), nullable=True
    )
    paciente_id = Column(
        Integer, ForeignKey("pacientes.paciente_id", ondelete="SET NULL"), nullable=True
    )

    paciente = relationship("Paciente")

    medicamento = relationship(
        "Medicamento", back_populates="exame_imagem"
    )  #  Para médicos se relacionarem com exames de imagem
    upload_imagem = relationship(
        "UploadExameImagem", back_populates="exames_imagem"
    )  #  Para a lógica de 'Uploads' se relacionar com exames de imagem
    resultados = relationship("ResultadoExameImagemIa", back_populates="exame_imagem")


class UploadExameImagem(Base):
    """Taabela que guarda caminhos de "upload' de imagens"""

    __tablename__ = "uploads_exame_imagem"

    upload_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    caminho_upload = Column(String(255), nullable=False)

    exame_imagem_id = Column(
        Integer, ForeignKey("exames_imagem.exame_id", ondelete="CASCADE")
    )  # Relacionando a imagem de upload a tabela de exames de imagem com ForeignKey
    exames_imagem = relationship("ExameImagem", back_populates="upload_imagem")


class ResultadoExameImagemIa(Base):
    """Tabela para salvar resultados de exames de imagem pelo modelo"""

    __tablename__ = "resultados_exame_imagem_ia"

    resultado_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    classe_predita = Column(String(100), nullable=False)
    confianca = Column(Float, nullable=False)

    probabilidades = Column(JSON, nullable=False)

    interpretacao = Column(String(255), nullable=True)

    data_analise = Column(DateTime, default=datetime.utcnow)

    #  Relacionando o resultado da análise do exame de imagem com a imagem
    exame_imagem_id = Column(
        Integer, ForeignKey("exames_imagem.exame_id", ondelete="CASCADE")
    )

    #  Relacionando Resultados com exames de imagem
    exame_imagem = relationship("ExameImagem", back_populates="resultados")
