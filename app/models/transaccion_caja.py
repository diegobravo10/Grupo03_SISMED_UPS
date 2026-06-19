from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class TransaccionCaja(Base):
    __tablename__ = "transacciones_caja"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(20), nullable=False)
    concepto = Column(String(300), nullable=False)
    monto = Column(Float, nullable=False, default=0.0)
    fecha = Column(Date, nullable=False)
    comprobante_id = Column(Integer, ForeignKey("comprobantes_venta.id"), nullable=True)
    fecha_creacion = Column(DateTime, server_default=func.now())

    comprobante = relationship("ComprobanteVenta", back_populates="transacciones")
