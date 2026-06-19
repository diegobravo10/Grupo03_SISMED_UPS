from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ComprobanteVenta(Base):
    __tablename__ = "comprobantes_venta"

    id = Column(Integer, primary_key=True, index=True)
    tipo_comprobante = Column(String(20), nullable=False)
    serie = Column(String(10), nullable=False)
    numero = Column(String(20), nullable=False)
    cliente_nombre = Column(String(200), nullable=False)
    cliente_documento = Column(String(20), nullable=False)
    fecha_emision = Column(Date, nullable=False)
    subtotal = Column(Float, nullable=False, default=0.0)
    igv = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    estado = Column(String(20), nullable=False, default="EMITIDO")
    fecha_creacion = Column(DateTime, server_default=func.now())

    transacciones = relationship("TransaccionCaja", back_populates="comprobante")
