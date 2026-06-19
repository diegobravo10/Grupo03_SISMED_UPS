from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConsultaMedicaBase(BaseModel):
    cita_id: int
    motivo: str | None = None
    anamnesis: str | None = None
    diagnostico: str | None = None
    observaciones: str | None = None
    tratamiento: str | None = None


class ConsultaMedicaCreate(ConsultaMedicaBase):
    pass


class ConsultaMedicaResponse(ConsultaMedicaBase):
    id: int
    paciente_id: int
    medico_id: int
    fecha_registro: datetime

    model_config = ConfigDict(from_attributes=True)
