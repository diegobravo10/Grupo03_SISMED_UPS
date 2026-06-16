from sqlalchemy.orm import Session

from app.models.cita import Cita
from app.repositories import cita as cita_repo
from app.repositories import medico as medico_repo
from app.repositories import paciente as paciente_repo
from app.schemas.cita import CitaCreate
from app.services.exceptions import EntidadNoEncontradaError, ReglaNegocioError

ESTADOS_VALIDOS = {"pendiente", "confirmada", "cancelada", "atendida"}

TRANSICIONES_VALIDAS = {
    "pendiente": {"confirmada", "cancelada"},
    "confirmada": {"atendida", "cancelada"},
    "cancelada": set(),
    "atendida": set(),
}


def agendar_cita(db: Session, cita: CitaCreate) -> Cita:
    if cita.hora_inicio >= cita.hora_fin:
        raise ReglaNegocioError("La hora de inicio debe ser anterior a la hora de fin")

    if paciente_repo.obtener_por_id(db, cita.paciente_id) is None:
        raise EntidadNoEncontradaError("Paciente no encontrado")

    if medico_repo.obtener_por_id(db, cita.medico_id) is None:
        raise EntidadNoEncontradaError("Médico no encontrado")

    cruce = cita_repo.buscar_cruce_horario(
        db, cita.medico_id, cita.fecha, cita.hora_inicio, cita.hora_fin
    )
    if cruce is not None:
        raise ReglaNegocioError("El médico ya tiene una cita registrada en ese horario")

    return cita_repo.crear_cita(db, cita)


def listar_citas(db: Session) -> list[Cita]:
    return cita_repo.listar_citas(db)


def buscar_cita_por_id(db: Session, cita_id: int) -> Cita:
    cita = cita_repo.obtener_cita_por_id(db, cita_id)
    if cita is None:
        raise EntidadNoEncontradaError("Cita no encontrada")
    return cita


def listar_citas_por_medico(db: Session, medico_id: int) -> list[Cita]:
    if medico_repo.obtener_por_id(db, medico_id) is None:
        raise EntidadNoEncontradaError("Médico no encontrado")
    return cita_repo.obtener_citas_por_medico(db, medico_id)


def listar_citas_por_paciente(db: Session, paciente_id: int) -> list[Cita]:
    if paciente_repo.obtener_por_id(db, paciente_id) is None:
        raise EntidadNoEncontradaError("Paciente no encontrado")
    return cita_repo.obtener_citas_por_paciente(db, paciente_id)


def cambiar_estado_cita(db: Session, cita_id: int, nuevo_estado: str) -> Cita:
    if nuevo_estado not in ESTADOS_VALIDOS:
        raise ReglaNegocioError(f"Estado '{nuevo_estado}' no es válido")

    cita = cita_repo.obtener_cita_por_id(db, cita_id)
    if cita is None:
        raise EntidadNoEncontradaError("Cita no encontrada")

    if nuevo_estado not in TRANSICIONES_VALIDAS[cita.estado]:
        raise ReglaNegocioError(
            f"No se puede cambiar la cita de '{cita.estado}' a '{nuevo_estado}'"
        )

    return cita_repo.actualizar_estado(db, cita_id, nuevo_estado)
