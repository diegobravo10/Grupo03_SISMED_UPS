from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CertificadoMedico(Base):
    __tablename__ = "certificados_medicos"

    id = Column(Integer, primary_key=True, index=True)
    consulta_id = Column(Integer, ForeignKey("consultas_medicas.id"), nullable=False)
    tipo = Column(String, nullable=False)
    contenido = Column(String, nullable=False)
    fecha_emision = Column(DateTime, server_default=func.now())

    consulta = relationship("ConsultaMedica", back_populates="certificados")
