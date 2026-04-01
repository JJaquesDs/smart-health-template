from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.connection import Base


class ExameImagem(Base):
    """ Tabela Base de Exames """

    __tablename__ = 'exames_imagem'

    exame_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(45), nullable=False)
    descricao = Column(String(45))
    link_imagem = Column(String(45))

    medicamento = relationship("Medicamento", back_populates="exame_imagem")            #  Para médicos se relacionarem com exames de imagem
    upload_imagem = relationship("UploadExameImagem", back_populates="exames_imagem")    #  Para a lógica de 'Uploads' se relacionar com exames de imagem


class UploadExameImagem(Base):
    """ Taabela que guarda caminhos de "upload' de imagens """

    __tablename__ = 'uploads_exame_imagem'

    upload_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(45), nullable=False)
    caminho_upload = Column(String(255), nullable=False)

    exame_imagem_id = Column(Integer, ForeignKey('exames_imagem.exame_id', ondelete="CASCADE"))  # Relacionando a imagem de upload a tabela de exames de imagem com ForeignKey


class ResultadoExameImagemIa(Base):
    """ Tabela para salvar resultados de exames de imagem pelo modelo """

    __tablename__ = 'resultados_exame_imagem_ia'

    resultado_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    risco = Column(Float, nullable=False)
    data_analise = Column(DateTime, default=datetime.utcnow)

    exame_imagem_id = Column(Integer, ForeignKey('exames_imagem.exame_id', ondelete="CASCADE"))             #  Relacionando o resultado da análise do exame de imagem com a imagem
    exame_imagem = relationship("ExameImagem", back_populates="resultados")    #  Relacionando Resultados com exames de imagem

    #  Ela ainda n tem schemas ou classe pública, pois não possui dados sensíveis como senhas
