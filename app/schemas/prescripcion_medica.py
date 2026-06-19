from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PrescripcionMedicaBase(BaseModel):
    consulta_id: int
    medicamento: str
    dosis: str | None = None
    frecuencia: str | None = None
    duracion: str | None = None
    indicaciones: str | None = None


class PrescripcionMedicaCreate(PrescripcionMedicaBase):
    pass


class PrescripcionMedicaResponse(PrescripcionMedicaBase):
    id: int
    fecha_prescripcion: datetime

    model_config = ConfigDict(from_attributes=True)
