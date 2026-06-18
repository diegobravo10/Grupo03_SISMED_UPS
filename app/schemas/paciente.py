from pydantic import BaseModel


class PacienteBase(BaseModel):
    cedula: str
    nombres: str
    apellidos: str
    telefono: str


class PacienteCreate(PacienteBase):
    pass


class PacienteResponse(PacienteBase):
    id: int

    class Config:
        from_attributes = True