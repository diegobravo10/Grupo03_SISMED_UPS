from datetime import date

from sqlalchemy.orm import Session

from app.models.transaccion_caja import TransaccionCaja
from app.schemas.transaccion_caja import TransaccionCajaCreate


def crear_transaccion(
    db: Session, data: TransaccionCajaCreate
) -> TransaccionCaja:
    transaccion = TransaccionCaja(**data.model_dump())
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion


def listar_ingresos_por_fecha(
    db: Session, fecha_inicio: date, fecha_fin: date
) -> list[TransaccionCaja]:
    return (
        db.query(TransaccionCaja)
        .filter(
            TransaccionCaja.tipo == "INGRESO",
            TransaccionCaja.fecha >= fecha_inicio,
            TransaccionCaja.fecha <= fecha_fin,
        )
        .all()
    )
