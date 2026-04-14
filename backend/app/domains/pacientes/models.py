from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.connection import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    paciente_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(45), nullable=False, unique=True)
    data_nascimento = Column(String(10), nullable=False)
    genero = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False, unique=True)
    telefone = Column(String(45), nullable=False)
    rua = Column(String(255), nullable=True)
    numero = Column(String(45), nullable=True)
    complemento = Column(String(255), nullable=True)
    cidade = Column(String(120), nullable=True)
    estado = Column(String(45), nullable=True)
    cep = Column(String(20), nullable=True)
    dados_clinicos = Column(Text, nullable=True)
    tipo_sanguineo = Column(String(10), nullable=True)
    ultimo_exame = Column(String(255), nullable=True)
    alergias = Column(Text, nullable=True)
    medicamentos = Column(Text, nullable=True)
    historico_medico = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)
    contato_emergencia_nome = Column(String(255), nullable=True)
    contato_emergencia_parentesco = Column(String(120), nullable=True)
    contato_emergencia_telefone = Column(String(45), nullable=True)
    rg = Column(String(45), nullable=True)
    data_cadastro = Column(String(45), nullable=True)
    endereco = Column(String(255), nullable=True)
    plano_saude = Column(Boolean, nullable=True)

    consultas = relationship("Consulta", back_populates="paciente")
