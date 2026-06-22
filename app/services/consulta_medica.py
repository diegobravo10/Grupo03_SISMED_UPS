from sqlalchemy.orm import Session

from app.models.consulta_medica import ConsultaMedica
from app.repositories import consulta_medica as consulta_repo
from app.repositories import cita as cita_repo
from app.repositories.medico import MedicoRepository as medico_repo
from app.repositories.paciente import PacienteRepository as paciente_repo
from app.schemas.consulta_medica import ConsultaMedicaCreate
from app.services.exceptions import EntidadNoEncontradaError, ReglaNegocioError


def registrar_consulta(db: Session, datos: ConsultaMedicaCreate) -> ConsultaMedica:
    cita = cita_repo.obtener_cita_por_id(db, datos.cita_id)
    if cita is None:
        raise EntidadNoEncontradaError("Cita no encontrada")

    if consulta_repo.obtener_por_cita_id(db, datos.cita_id) is not None:
        raise ReglaNegocioError("Ya existe una consulta registrada para esta cita")

    if paciente_repo.obtener_por_id(db, cita.paciente_id) is None:
        raise EntidadNoEncontradaError("Paciente no encontrado")

    if medico_repo.obtener_por_id(db, cita.medico_id) is None:
        raise EntidadNoEncontradaError("Médico no encontrado")

    consulta = ConsultaMedica(
        cita_id=datos.cita_id,
        paciente_id=cita.paciente_id,
        medico_id=cita.medico_id,
        motivo=datos.motivo,
        anamnesis=datos.anamnesis,
        diagnostico=datos.diagnostico,
        observaciones=datos.observaciones,
        tratamiento=datos.tratamiento,
    )
    return consulta_repo.crear_consulta(db, consulta)


def listar_consultas(db: Session) -> list[ConsultaMedica]:
    return consulta_repo.listar_todos(db)


def buscar_por_id(db: Session, consulta_id: int) -> ConsultaMedica:
    consulta = consulta_repo.obtener_por_id(db, consulta_id)
    if consulta is None:
        raise EntidadNoEncontradaError("Consulta no encontrada")
    return consulta


def listar_por_paciente(db: Session, paciente_id: int) -> list[ConsultaMedica]:
    if paciente_repo.obtener_por_id(db, paciente_id) is None:
        raise EntidadNoEncontradaError("Paciente no encontrado")
    return consulta_repo.listar_por_paciente(db, paciente_id)


def buscar_por_cita(db: Session, cita_id: int) -> ConsultaMedica:
    if cita_repo.obtener_cita_por_id(db, cita_id) is None:
        raise EntidadNoEncontradaError("Cita no encontrada")
    consulta = consulta_repo.obtener_por_cita_id(db, cita_id)
    if consulta is None:
        raise EntidadNoEncontradaError("No hay consulta registrada para esta cita")
    return consulta
