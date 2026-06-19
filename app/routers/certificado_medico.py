from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.certificado_medico import CertificadoMedicoCreate, CertificadoMedicoResponse
from app.services import certificado_medico as certificado_service
from app.services.exceptions import EntidadNoEncontradaError

router = APIRouter(prefix="/certificados", tags=["Certificados Médicos"])


@router.post("/", response_model=CertificadoMedicoResponse, status_code=status.HTTP_201_CREATED)
def crear_certificado(datos: CertificadoMedicoCreate, db: Session = Depends(get_db)):
    try:
        return certificado_service.crear_certificado(db, datos)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/consulta/{consulta_id}", response_model=list[CertificadoMedicoResponse])
def listar_certificados_por_consulta(consulta_id: int, db: Session = Depends(get_db)):
    try:
        return certificado_service.listar_por_consulta(db, consulta_id)
    except EntidadNoEncontradaError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
