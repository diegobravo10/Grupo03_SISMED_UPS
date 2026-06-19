from datetime import date

from sqlalchemy.orm import Session

from app.models.comprobante_venta import ComprobanteVenta
from app.schemas.comprobante_venta import ComprobanteVentaCreate


def crear_comprobante(db: Session, data: ComprobanteVentaCreate) -> ComprobanteVenta:
    comprobante = ComprobanteVenta(**data.model_dump())
    db.add(comprobante)
    db.commit()
    db.refresh(comprobante)
    return comprobante


def listar_comprobantes(db: Session) -> list[ComprobanteVenta]:
    return db.query(ComprobanteVenta).all()


def obtener_comprobante_por_id(
    db: Session, comprobante_id: int
) -> ComprobanteVenta | None:
    return (
        db.query(ComprobanteVenta)
        .filter(ComprobanteVenta.id == comprobante_id)
        .first()
    )
