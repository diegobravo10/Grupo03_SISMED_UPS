from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.comprobante_venta import ComprobanteVentaCreate, ComprobanteVentaResponse
from app.schemas.transaccion_caja import TransaccionCajaCreate, TransaccionCajaResponse
from app.services import administrativo as admin_service
from app.services.exceptions import EntidadNoEncontradaError, ReglaNegocioError

router = APIRouter(prefix="/admin", tags=["Administrativo"])


@router.post(
    "/comprobantes/",
    response_model=ComprobanteVentaResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_comprobante(
    data: ComprobanteVentaCreate, db: Session = Depends(get_db)
):
    try:
        return admin_service.registrar_comprobante(db, data)
    except ReglaNegocioError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/comprobantes/",
    response_model=list[ComprobanteVentaResponse],
)
def listar_comprobantes(db: Session = Depends(get_db)):
    return admin_service.listar_comprobantes(db)


@router.post(
    "/caja/ingresos",
    response_model=TransaccionCajaResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_ingreso(
    data: TransaccionCajaCreate, db: Session = Depends(get_db)
):
    try:
        return admin_service.registrar_ingreso(db, data)
    except ReglaNegocioError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post(
    "/caja/egresos",
    response_model=TransaccionCajaResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_egreso(
    data: TransaccionCajaCreate, db: Session = Depends(get_db)
):
    try:
        return admin_service.registrar_egreso(db, data)
    except ReglaNegocioError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.get(
    "/caja/ingresos",
    response_model=list[TransaccionCajaResponse],
)
def consultar_ingresos_por_fecha(
    fecha_inicio: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_fin: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    try:
        return admin_service.consultar_ingresos_por_fecha(
            db, fecha_inicio, fecha_fin
        )
    except ReglaNegocioError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
