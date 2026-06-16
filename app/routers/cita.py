from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.cita import CitaCambioEstado, CitaCreate, CitaResponse
from app.services import cita as cita_service
from app.services.exceptions import EntidadNoEncontradaError, ReglaNegocioError

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    try:
        return cita_service.agendar_cita(db, cita)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[CitaResponse])
def listar_citas(db: Session = Depends(get_db)):
    return cita_service.listar_citas(db)


@router.get("/{cita_id}", response_model=CitaResponse)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    try:
        return cita_service.buscar_cita_por_id(db, cita_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/medico/{medico_id}", response_model=list[CitaResponse])
def listar_citas_por_medico(medico_id: int, db: Session = Depends(get_db)):
    try:
        return cita_service.listar_citas_por_medico(db, medico_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/paciente/{paciente_id}", response_model=list[CitaResponse])
def listar_citas_por_paciente(paciente_id: int, db: Session = Depends(get_db)):
    try:
        return cita_service.listar_citas_por_paciente(db, paciente_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{cita_id}/estado", response_model=CitaResponse)
def cambiar_estado_cita(
    cita_id: int, cambio: CitaCambioEstado, db: Session = Depends(get_db)
):
    try:
        return cita_service.cambiar_estado_cita(db, cita_id, cambio.estado)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
