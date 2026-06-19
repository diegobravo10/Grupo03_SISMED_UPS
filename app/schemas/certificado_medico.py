from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CertificadoMedicoBase(BaseModel):
    consulta_id: int
    tipo: str
    contenido: str


class CertificadoMedicoCreate(CertificadoMedicoBase):
    pass


class CertificadoMedicoResponse(CertificadoMedicoBase):
    id: int
    fecha_emision: datetime

    model_config = ConfigDict(from_attributes=True)
