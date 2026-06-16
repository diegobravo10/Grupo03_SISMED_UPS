from sqlalchemy.orm import Session

from app.models.medico import Medico


def obtener_por_id(db: Session, medico_id: int) -> Medico | None:
    return db.query(Medico).filter(Medico.id == medico_id).first()
