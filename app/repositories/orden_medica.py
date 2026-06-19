from sqlalchemy.orm import Session

from app.models.orden_medica import OrdenMedica


def crear(db: Session, orden: OrdenMedica) -> OrdenMedica:
    db.add(orden)
    db.commit()
    db.refresh(orden)
    return orden


def listar_por_consulta(db: Session, consulta_id: int) -> list[OrdenMedica]:
    return db.query(OrdenMedica).filter(OrdenMedica.consulta_id == consulta_id).all()


def obtener_por_id(db: Session, orden_id: int) -> OrdenMedica | None:
    return db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
