from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# from app.database.connection import Base


class Area(Base):
    __tablename__ = "areas"

    area_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(45), nullable=False)
    status = Column(String(45), nullable=False)

    medicos = relationship("Medico", back_populates="area")