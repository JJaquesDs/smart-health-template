from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


from app.core.connection import Base


class DoencaProntuario(Base):
    """ Classe que une tabela doencas e pronturarios por ser uma relacao muitos para muitos """

    __tablename__ = "doenca_prontuario"

    doenca_prontuario_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    doenca_id = Column(Integer, ForeignKey('doencas.doenca_id', ondelete="CASCADE"), nullable=False)
    prontuario_id = Column(Integer, ForeignKey('prontuarios.prontuario_id', ondelete="CASCADE"), nullable=False)

    # RELACIONAMENTOS
    doenca = relationship("Doencas", back_populates="doenca_prontuarios")
    prontuario = relationship("Prontuario", back_populates="doenca_prontuarios")