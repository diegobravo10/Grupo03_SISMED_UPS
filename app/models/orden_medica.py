from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class OrdenMedica(Base):
    __tablename__ = "ordenes_medicas"

    id = Column(Integer, primary_key=True, index=True)
    consulta_id = Column(Integer, ForeignKey("consultas_medicas.id"), nullable=False)
    tipo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    indicaciones = Column(String, nullable=True)
    fecha_orden = Column(DateTime, server_default=func.now())

    consulta = relationship("ConsultaMedica", back_populates="ordenes")
