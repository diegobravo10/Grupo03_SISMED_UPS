from pydantic import BaseModel

class PacienteBase(BaseModel):
    nombres: str
    apellidos: str
    cedula: str
    telefono: str

class PacienteCreate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    id: int

    class Config:
        from_attributes = True