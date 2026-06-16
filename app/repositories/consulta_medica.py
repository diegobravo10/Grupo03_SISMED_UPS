from sqlalchemy.orm import Session

from app.models.consulta_medica import ConsultaMedica


def obtener_por_cita_id(db: Session, cita_id: int) -> ConsultaMedica | None:
    return db.query(ConsultaMedica).filter(ConsultaMedica.cita_id == cita_id).first()
