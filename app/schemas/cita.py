from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict


class CitaBase(BaseModel):
    paciente_id: int
    medico_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    motivo: str | None = None


class CitaCreate(CitaBase):
    pass


class CitaResponse(CitaBase):
    id: int
    estado: str
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)


class CitaCambioEstado(BaseModel):
    estado: str
