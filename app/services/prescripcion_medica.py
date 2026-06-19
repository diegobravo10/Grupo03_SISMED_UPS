from sqlalchemy.orm import Session

from app.models.prescripcion_medica import PrescripcionMedica
from app.repositories import consulta_medica as consulta_repo
from app.repositories import prescripcion_medica as prescripcion_repo
from app.schemas.prescripcion_medica import PrescripcionMedicaCreate
from app.services.exceptions import EntidadNoEncontradaError


def crear_prescripcion(db: Session, datos: PrescripcionMedicaCreate) -> PrescripcionMedica:
    if consulta_repo.obtener_por_id(db, datos.consulta_id) is None:
        raise EntidadNoEncontradaError("Consulta no encontrada")

    prescripcion = PrescripcionMedica(**datos.model_dump())
    return prescripcion_repo.crear(db, prescripcion)


def listar_por_consulta(db: Session, consulta_id: int) -> list[PrescripcionMedica]:
    if consulta_repo.obtener_por_id(db, consulta_id) is None:
        raise EntidadNoEncontradaError("Consulta no encontrada")
    return prescripcion_repo.listar_por_consulta(db, consulta_id)
