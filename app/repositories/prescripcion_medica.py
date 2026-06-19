from sqlalchemy.orm import Session

from app.models.prescripcion_medica import PrescripcionMedica


def crear(db: Session, prescripcion: PrescripcionMedica) -> PrescripcionMedica:
    db.add(prescripcion)
    db.commit()
    db.refresh(prescripcion)
    return prescripcion


def listar_por_consulta(db: Session, consulta_id: int) -> list[PrescripcionMedica]:
    return db.query(PrescripcionMedica).filter(PrescripcionMedica.consulta_id == consulta_id).all()


def obtener_por_id(db: Session, prescripcion_id: int) -> PrescripcionMedica | None:
    return db.query(PrescripcionMedica).filter(PrescripcionMedica.id == prescripcion_id).first()
