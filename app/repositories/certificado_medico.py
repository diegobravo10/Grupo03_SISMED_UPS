from sqlalchemy.orm import Session

from app.models.certificado_medico import CertificadoMedico


def crear(db: Session, certificado: CertificadoMedico) -> CertificadoMedico:
    db.add(certificado)
    db.commit()
    db.refresh(certificado)
    return certificado


def listar_por_consulta(db: Session, consulta_id: int) -> list[CertificadoMedico]:
    return db.query(CertificadoMedico).filter(CertificadoMedico.consulta_id == consulta_id).all()


def obtener_por_id(db: Session, certificado_id: int) -> CertificadoMedico | None:
    return db.query(CertificadoMedico).filter(CertificadoMedico.id == certificado_id).first()
