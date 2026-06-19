from sqlalchemy.orm import Session

from app.models.certificado_medico import CertificadoMedico
from app.repositories import certificado_medico as certificado_repo
from app.repositories import consulta_medica as consulta_repo
from app.schemas.certificado_medico import CertificadoMedicoCreate
from app.services.exceptions import EntidadNoEncontradaError


def crear_certificado(db: Session, datos: CertificadoMedicoCreate) -> CertificadoMedico:
    if consulta_repo.obtener_por_id(db, datos.consulta_id) is None:
        raise EntidadNoEncontradaError("Consulta no encontrada")

    certificado = CertificadoMedico(**datos.model_dump())
    return certificado_repo.crear(db, certificado)


def listar_por_consulta(db: Session, consulta_id: int) -> list[CertificadoMedico]:
    if consulta_repo.obtener_por_id(db, consulta_id) is None:
        raise EntidadNoEncontradaError("Consulta no encontrada")
    return certificado_repo.listar_por_consulta(db, consulta_id)
