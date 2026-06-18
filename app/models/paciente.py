from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    telefono = Column(String, nullable=True)

    fecha_registro = Column(
        DateTime,
        server_default=func.now()
    )

    citas = relationship(
        "Cita",
        back_populates="paciente"
    )

    consultas = relationship(
        "ConsultaMedica",
        back_populates="paciente"
    )