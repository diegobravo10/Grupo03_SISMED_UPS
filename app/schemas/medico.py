from pydantic import BaseModel

class MedicoBase(BaseModel):
    nombres: str
    apellidos: str
    especialidad: str

class MedicoCreate(MedicoBase):
    pass

class MedicoResponse(MedicoBase):
    id: int

    class Config:
        from_attributes = True