from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base

class Medico(Base):

    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)

    nombres = Column(String(100))
    especialidad = Column(String(100))

    citas = relationship(
        "Cita",
        back_populates="medico"
    )

    consultas = relationship(
        "ConsultaMedica",
        back_populates="medico"
    )