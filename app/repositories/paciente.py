from sqlalchemy.orm import Session

from app.models.paciente import Paciente


def obtener_por_id(db: Session, paciente_id: int) -> Paciente | None:
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()
