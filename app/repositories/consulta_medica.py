from sqlalchemy.orm import Session

from app.models.consulta_medica import ConsultaMedica


def crear_consulta(db: Session, consulta: ConsultaMedica) -> ConsultaMedica:
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


def obtener_por_id(db: Session, consulta_id: int) -> ConsultaMedica | None:
    return db.query(ConsultaMedica).filter(ConsultaMedica.id == consulta_id).first()


def obtener_por_cita_id(db: Session, cita_id: int) -> ConsultaMedica | None:
    return db.query(ConsultaMedica).filter(ConsultaMedica.cita_id == cita_id).first()


def listar_todos(db: Session) -> list[ConsultaMedica]:
    return db.query(ConsultaMedica).all()


def listar_por_paciente(db: Session, paciente_id: int) -> list[ConsultaMedica]:
    return db.query(ConsultaMedica).filter(ConsultaMedica.paciente_id == paciente_id).all()
