from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.medico_schema import (
    MedicoCreate,
    MedicoResponse
)

from app.services.medico_service import (
    MedicoService
)

router = APIRouter(
    prefix="/medicos",
    tags=["Medicos"]
)


@router.post(
    "/",
    response_model=MedicoResponse
)
def crear_medico(
    medico: MedicoCreate,
    db: Session = Depends(get_db)
):
    return MedicoService.crear_medico(
        db,
        medico
    )


@router.get(
    "/",
    response_model=list[MedicoResponse]
)
def listar_medicos(
    db: Session = Depends(get_db)
):
    return MedicoService.listar_medicos(db)


@router.get(
    "/{medico_id}",
    response_model=MedicoResponse
)
def obtener_medico(
    medico_id: int,
    db: Session = Depends(get_db)
):
    return MedicoService.obtener_medico(
        db,
        medico_id
    )


@router.put(
    "/{medico_id}",
    response_model=MedicoResponse
)
def actualizar_medico(
    medico_id: int,
    medico: MedicoCreate,
    db: Session = Depends(get_db)
):
    return MedicoService.actualizar_medico(
        db,
        medico_id,
        medico
    )


@router.delete(
    "/{medico_id}"
)
def eliminar_medico(
    medico_id: int,
    db: Session = Depends(get_db)
):
    return MedicoService.eliminar_medico(
        db,
        medico_id
    )