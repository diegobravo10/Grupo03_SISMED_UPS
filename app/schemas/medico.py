from pydantic import BaseModel, ConfigDict


class MedicoMinimo(BaseModel):
    """Schema mínimo usado para validar existencia del médico."""

    id: int
    nombres: str
    apellidos: str
    especialidad: str

    model_config = ConfigDict(from_attributes=True)
