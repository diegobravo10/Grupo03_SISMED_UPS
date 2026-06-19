from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.consulta_medica import ConsultaMedicaCreate, ConsultaMedicaResponse
from app.services import consulta_medica as consulta_service
from app.services.exceptions import EntidadNoEncontradaError, ReglaNegocioError

router = APIRouter(prefix="/consultas", tags=["Consultas Médicas"])


@router.post("/", response_model=ConsultaMedicaResponse, status_code=status.HTTP_201_CREATED)
def registrar_consulta(datos: ConsultaMedicaCreate, db: Session = Depends(get_db)):
    try:
        return consulta_service.registrar_consulta(db, datos)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ReglaNegocioError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[ConsultaMedicaResponse])
def listar_consultas(db: Session = Depends(get_db)):
    return consulta_service.listar_consultas(db)


@router.get("/{consulta_id}", response_model=ConsultaMedicaResponse)
def obtener_consulta(consulta_id: int, db: Session = Depends(get_db)):
    try:
        return consulta_service.buscar_por_id(db, consulta_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/paciente/{paciente_id}", response_model=list[ConsultaMedicaResponse])
def listar_consultas_por_paciente(paciente_id: int, db: Session = Depends(get_db)):
    try:
        return consulta_service.listar_por_paciente(db, paciente_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/cita/{cita_id}", response_model=ConsultaMedicaResponse)
def obtener_consulta_por_cita(cita_id: int, db: Session = Depends(get_db)):
    try:
        return consulta_service.buscar_por_cita(db, cita_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
