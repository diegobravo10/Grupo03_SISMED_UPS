from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    motivo = Column(String, nullable=True)
    estado = Column(String, nullable=False, default="SEPARADA")
    fecha_creacion = Column(DateTime, server_default=func.now())

    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")
    consulta = relationship("ConsultaMedica", back_populates="cita", uselist=False)
