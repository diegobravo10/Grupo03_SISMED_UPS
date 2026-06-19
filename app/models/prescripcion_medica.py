from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PrescripcionMedica(Base):
    __tablename__ = "prescripciones_medicas"

    id = Column(Integer, primary_key=True, index=True)
    consulta_id = Column(Integer, ForeignKey("consultas_medicas.id"), nullable=False)
    medicamento = Column(String, nullable=False)
    dosis = Column(String, nullable=True)
    frecuencia = Column(String, nullable=True)
    duracion = Column(String, nullable=True)
    indicaciones = Column(String, nullable=True)
    fecha_prescripcion = Column(DateTime, server_default=func.now())

    consulta = relationship("ConsultaMedica", back_populates="prescripciones")
