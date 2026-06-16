from pydantic import BaseModel, ConfigDict


class PacienteMinimo(BaseModel):
    """Schema mínimo usado para validar existencia del paciente."""

    id: int
    nombres: str
    apellidos: str

    model_config = ConfigDict(from_attributes=True)
