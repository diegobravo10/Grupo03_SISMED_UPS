from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.prescripcion_medica import PrescripcionMedicaCreate, PrescripcionMedicaResponse
from app.services import prescripcion_medica as prescripcion_service
from app.services.exceptions import EntidadNoEncontradaError

router = APIRouter(prefix="/prescripciones", tags=["Prescripciones Médicas"])


@router.post("/", response_model=PrescripcionMedicaResponse, status_code=status.HTTP_201_CREATED)
def crear_prescripcion(datos: PrescripcionMedicaCreate, db: Session = Depends(get_db)):
    try:
        return prescripcion_service.crear_prescripcion(db, datos)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/consulta/{consulta_id}", response_model=list[PrescripcionMedicaResponse])
def listar_prescripciones_por_consulta(consulta_id: int, db: Session = Depends(get_db)):
    try:
        return prescripcion_service.listar_por_consulta(db, consulta_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
