from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.orden_medica import OrdenMedicaCreate, OrdenMedicaResponse
from app.services import orden_medica as orden_service
from app.services.exceptions import EntidadNoEncontradaError

router = APIRouter(prefix="/ordenes", tags=["Órdenes Médicas"])


@router.post("/", response_model=OrdenMedicaResponse, status_code=status.HTTP_201_CREATED)
def crear_orden(datos: OrdenMedicaCreate, db: Session = Depends(get_db)):
    try:
        return orden_service.crear_orden(db, datos)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/consulta/{consulta_id}", response_model=list[OrdenMedicaResponse])
def listar_ordenes_por_consulta(consulta_id: int, db: Session = Depends(get_db)):
    try:
        return orden_service.listar_por_consulta(db, consulta_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
