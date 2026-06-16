from sqlalchemy.orm import Session

from app.models.cita import Cita
from app.repositories import cita as cita_repo
from app.repositories import consulta_medica as consulta_repo
from app.repositories import medico as medico_repo
from app.repositories import paciente as paciente_repo
from app.schemas.cita import CitaCreate
from app.services.exceptions import EntidadNoEncontradaError, ReglaNegocioError

ESTADO_SEPARADA = "SEPARADA"
ESTADO_CONFIRMADA = "CONFIRMADA"
ESTADO_EN_SALA_ESPERA = "EN_SALA_ESPERA"
ESTADO_ATENDIDA = "ATENDIDA"
ESTADO_CANCELADA = "CANCELADA"
ESTADO_NO_ASISTIO = "NO_ASISTIO"

ESTADOS_VALIDOS = {
    ESTADO_SEPARADA,
    ESTADO_CONFIRMADA,
    ESTADO_EN_SALA_ESPERA,
    ESTADO_ATENDIDA,
    ESTADO_CANCELADA,
    ESTADO_NO_ASISTIO,
}

TRANSICIONES_VALIDAS = {
    ESTADO_SEPARADA: {ESTADO_CONFIRMADA, ESTADO_CANCELADA, ESTADO_NO_ASISTIO},
    ESTADO_CONFIRMADA: {ESTADO_EN_SALA_ESPERA, ESTADO_CANCELADA, ESTADO_NO_ASISTIO},
    ESTADO_EN_SALA_ESPERA: {ESTADO_ATENDIDA, ESTADO_NO_ASISTIO},
    ESTADO_ATENDIDA: set(),
    ESTADO_CANCELADA: set(),
    ESTADO_NO_ASISTIO: set(),
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

    if nuevo_estado == ESTADO_ATENDIDA:
        if consulta_repo.obtener_por_cita_id(db, cita_id) is None:
            raise ReglaNegocioError(
                "No se puede marcar la cita como ATENDIDA sin una consulta médica asociada"
            )

    return cita_repo.actualizar_estado(db, cita_id, nuevo_estado)
