from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ComprobanteVentaBase(BaseModel):
    tipo_comprobante: str
    serie: str
    numero: str
    cliente_nombre: str
    cliente_documento: str
    fecha_emision: date
    subtotal: float
    igv: float
    total: float


class ComprobanteVentaCreate(ComprobanteVentaBase):
    pass


class ComprobanteVentaResponse(ComprobanteVentaBase):
    id: int
    estado: str
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)
