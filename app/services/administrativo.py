from datetime import date

from sqlalchemy.orm import Session

from app.repositories import comprobante_venta as comprobante_repo
from app.repositories import transaccion_caja as transaccion_repo
from app.schemas.comprobante_venta import ComprobanteVentaCreate
from app.schemas.transaccion_caja import TransaccionCajaCreate
from app.models.comprobante_venta import ComprobanteVenta
from app.models.transaccion_caja import TransaccionCaja
from app.services.exceptions import ReglaNegocioError


def registrar_comprobante(
    db: Session, data: ComprobanteVentaCreate
) -> ComprobanteVenta:
    if data.total != round(data.subtotal + data.igv, 2):
        raise ReglaNegocioError(
            "El total no coincide con la suma del subtotal e IGV"
        )

    comprobante = comprobante_repo.crear_comprobante(db, data)

    transaccion_data = TransaccionCajaCreate(
        tipo="INGRESO",
        concepto=f"Venta - {data.tipo_comprobante} {data.serie}-{data.numero}",
        monto=data.total,
        fecha=data.fecha_emision,
        comprobante_id=comprobante.id,
    )
    transaccion_repo.crear_transaccion(db, transaccion_data)

    return comprobante


def listar_comprobantes(db: Session) -> list[ComprobanteVenta]:
    return comprobante_repo.listar_comprobantes(db)


def registrar_ingreso(db: Session, data: TransaccionCajaCreate) -> TransaccionCaja:
    if data.tipo != "INGRESO":
        raise ReglaNegocioError("El tipo de transacción debe ser INGRESO")
    if data.monto <= 0:
        raise ReglaNegocioError("El monto del ingreso debe ser mayor a cero")
    return transaccion_repo.crear_transaccion(db, data)


def registrar_egreso(db: Session, data: TransaccionCajaCreate) -> TransaccionCaja:
    if data.tipo != "EGRESO":
        raise ReglaNegocioError("El tipo de transacción debe ser EGRESO")
    if data.monto <= 0:
        raise ReglaNegocioError("El monto del egreso debe ser mayor a cero")
    return transaccion_repo.crear_transaccion(db, data)


def consultar_ingresos_por_fecha(
    db: Session, fecha_inicio: date, fecha_fin: date
) -> list[TransaccionCaja]:
    if fecha_inicio > fecha_fin:
        raise ReglaNegocioError(
            "La fecha de inicio no puede ser posterior a la fecha de fin"
        )
    return transaccion_repo.listar_ingresos_por_fecha(db, fecha_inicio, fecha_fin)
