from datetime import date, time

from sqlalchemy.orm import Session

from app.models.cita import Cita
from app.schemas.cita import CitaCreate

ESTADO_CANCELADA = "CANCELADA"


def crear_cita(db: Session, cita: CitaCreate) -> Cita:
    nueva_cita = Cita(**cita.model_dump())
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita


def listar_citas(db: Session) -> list[Cita]:
    return db.query(Cita).all()


def obtener_cita_por_id(db: Session, cita_id: int) -> Cita | None:
    return db.query(Cita).filter(Cita.id == cita_id).first()


def obtener_citas_por_medico(db: Session, medico_id: int) -> list[Cita]:
    return db.query(Cita).filter(Cita.medico_id == medico_id).all()


def obtener_citas_por_paciente(db: Session, paciente_id: int) -> list[Cita]:
    return db.query(Cita).filter(Cita.paciente_id == paciente_id).all()


def buscar_cruce_horario(
    db: Session,
    medico_id: int,
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    excluir_cita_id: int | None = None,
) -> Cita | None:
    """Busca una cita existente del médico que se solape con el rango dado."""
    query = db.query(Cita).filter(
        Cita.medico_id == medico_id,
        Cita.fecha == fecha,
        Cita.estado != ESTADO_CANCELADA,
        Cita.hora_inicio < hora_fin,
        Cita.hora_fin > hora_inicio,
    )
    if excluir_cita_id is not None:
        query = query.filter(Cita.id != excluir_cita_id)
    return query.first()


def actualizar_estado(db: Session, cita_id: int, nuevo_estado: str) -> Cita | None:
    cita = obtener_cita_por_id(db, cita_id)
    if cita is None:
        return None
    cita.estado = nuevo_estado
    db.commit()
    db.refresh(cita)
    return cita
