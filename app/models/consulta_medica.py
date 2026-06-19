from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ConsultaMedica(Base):
    __tablename__ = "consultas_medicas"

    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, ForeignKey("citas.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    motivo = Column(String, nullable=True)
    anamnesis = Column(String, nullable=True)
    diagnostico = Column(String, nullable=True)
    observaciones = Column(String, nullable=True)
    tratamiento = Column(String, nullable=True)
    fecha_registro = Column(DateTime, server_default=func.now())

    cita = relationship("Cita", back_populates="consulta")
    paciente = relationship("Paciente", back_populates="consultas")
    medico = relationship("Medico", back_populates="consultas")
    prescripciones = relationship("PrescripcionMedica", back_populates="consulta", cascade="all, delete-orphan")
    ordenes = relationship("OrdenMedica", back_populates="consulta", cascade="all, delete-orphan")
    certificados = relationship("CertificadoMedico", back_populates="consulta", cascade="all, delete-orphan")
