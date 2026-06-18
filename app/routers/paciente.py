from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.paciente import (
    PacienteCreate,
    PacienteResponse
)
from app.services.paciente import PacienteService

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


@router.get(
    "/",
    response_model=list[PacienteResponse]
)
def listar_pacientes(
    db: Session = Depends(get_db)
):
    return PacienteService.listar_pacientes(db)


@router.get(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def obtener_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    return PacienteService.obtener_paciente(
        db,
        paciente_id
    )


@router.put(
    "/{paciente_id}",
    response_model=PacienteResponse
)
def actualizar_paciente(
    paciente_id: int,
    paciente: PacienteCreate,
    db: Session = Depends(get_db)
):
    return PacienteService.actualizar_paciente(
        db,
        paciente_id,
        paciente
    )


@router.delete(
    "/{paciente_id}"
)
def eliminar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    return PacienteService.eliminar_paciente(
        db,
        paciente_id
    )