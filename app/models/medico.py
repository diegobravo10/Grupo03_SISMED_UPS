from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)
    telefono = Column(String, nullable=True)
    correo = Column(String, nullable=True)
    estado = Column(String, nullable=False, default="activo")

    citas = relationship("Cita", back_populates="medico")
    consultas = relationship("ConsultaMedica", back_populates="medico")
