from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.connection import Base


class Doencas(Base):
    __tablename__ = "doencas"

    doenca_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    status = Column(String(15), nullable=False)

    doenca_prontuarios = relationship("DoencaProntuario", back_populates="doenca")