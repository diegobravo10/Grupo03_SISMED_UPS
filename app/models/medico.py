from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base

class Medico(Base):

    __tablename__ = "medicos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombres = Column(String(100))
    especialidad = Column(String(100))