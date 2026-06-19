from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TransaccionCajaBase(BaseModel):
    tipo: str
    concepto: str
    monto: float
    fecha: date
    comprobante_id: int | None = None


class TransaccionCajaCreate(TransaccionCajaBase):
    pass


class TransaccionCajaResponse(TransaccionCajaBase):
    id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)


class ConsultaIngresosParams(BaseModel):
    fecha_inicio: date = Field(default=..., description="Fecha de inicio del rango")
    fecha_fin: date = Field(default=..., description="Fecha de fin del rango")
