from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrdenMedicaBase(BaseModel):
    consulta_id: int
    tipo: str
    descripcion: str
    indicaciones: str | None = None


class OrdenMedicaCreate(OrdenMedicaBase):
    pass


class OrdenMedicaResponse(OrdenMedicaBase):
    id: int
    fecha_orden: datetime

    model_config = ConfigDict(from_attributes=True)
