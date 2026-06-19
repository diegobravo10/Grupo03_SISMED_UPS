from sqlalchemy.orm import Session

from app.models.orden_medica import OrdenMedica
from app.repositories import consulta_medica as consulta_repo
from app.repositories import orden_medica as orden_repo
from app.schemas.orden_medica import OrdenMedicaCreate
from app.services.exceptions import EntidadNoEncontradaError


def crear_orden(db: Session, datos: OrdenMedicaCreate) -> OrdenMedica:
    if consulta_repo.obtener_por_id(db, datos.consulta_id) is None:
        raise EntidadNoEncontradaError("Consulta no encontrada")

    orden = OrdenMedica(**datos.model_dump())
    return orden_repo.crear(db, orden)


def listar_por_consulta(db: Session, consulta_id: int) -> list[OrdenMedica]:
    if consulta_repo.obtener_por_id(db, consulta_id) is None:
        raise EntidadNoEncontradaError("Consulta no encontrada")
    return orden_repo.listar_por_consulta(db, consulta_id)
