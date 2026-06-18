from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.paciente_schema import (
    PacienteCreate,
    PacienteResponse
)

from app.services.paciente_service import PacienteService

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

@router.post(
    "/",
    response_model=PacienteResponse
)
def crear_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db)
):
    return PacienteService.crear_paciente(
        db,
        paciente
    )