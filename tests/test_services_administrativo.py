from datetime import date

import pytest

from app.schemas.comprobante_venta import ComprobanteVentaCreate
from app.schemas.transaccion_caja import TransaccionCajaCreate
from app.services import administrativo as admin_service
from app.services.exceptions import ReglaNegocioError


def comprobante_valido() -> ComprobanteVentaCreate:
    return ComprobanteVentaCreate(
        tipo_comprobante="BOLETA",
        serie="B001",
        numero="00000001",
        cliente_nombre="Juan Pérez",
        cliente_documento="0102030405",
        fecha_emision=date(2025, 1, 15),
        subtotal=100.0,
        igv=18.0,
        total=118.0,
    )


def transaccion_ingreso_valida() -> TransaccionCajaCreate:
    return TransaccionCajaCreate(
        tipo="INGRESO",
        concepto="Venta de producto X",
        monto=500.0,
        fecha=date(2025, 1, 15),
    )


def transaccion_egreso_valida() -> TransaccionCajaCreate:
    return TransaccionCajaCreate(
        tipo="EGRESO",
        concepto="Pago de servicios",
        monto=200.0,
        fecha=date(2025, 1, 15),
    )


# -- Comprobantes ------------------------------------------------------------------


def test_registrar_comprobante_exitoso(db_session):
    data = comprobante_valido()
    comprobante = admin_service.registrar_comprobante(db_session, data)

    assert comprobante.id is not None
    assert comprobante.tipo_comprobante == "BOLETA"
    assert comprobante.serie == "B001"
    assert comprobante.numero == "00000001"
    assert comprobante.total == 118.0


def test_registrar_comprobante_total_invalido(db_session):
    data = comprobante_valido()
    data.total = 999.0

    with pytest.raises(ReglaNegocioError) as exc:
        admin_service.registrar_comprobante(db_session, data)
    assert "total no coincide" in str(exc.value).lower()


def test_listar_comprobantes(db_session):
    data = comprobante_valido()
    admin_service.registrar_comprobante(db_session, data)

    resultado = admin_service.listar_comprobantes(db_session)
    assert len(resultado) == 1
    assert resultado[0].tipo_comprobante == "BOLETA"


# -- Caja: Ingresos ----------------------------------------------------------------


def test_registrar_ingreso_exitoso(db_session):
    data = transaccion_ingreso_valida()
    transaccion = admin_service.registrar_ingreso(db_session, data)

    assert transaccion.id is not None
    assert transaccion.tipo == "INGRESO"
    assert transaccion.monto == 500.0


def test_registrar_ingreso_tipo_invalido(db_session):
    data = transaccion_ingreso_valida()
    data.tipo = "EGRESO"

    with pytest.raises(ReglaNegocioError) as exc:
        admin_service.registrar_ingreso(db_session, data)
    assert "debe ser ingreso" in str(exc.value).lower()


def test_registrar_ingreso_monto_cero(db_session):
    data = transaccion_ingreso_valida()
    data.monto = 0

    with pytest.raises(ReglaNegocioError) as exc:
        admin_service.registrar_ingreso(db_session, data)
    assert "mayor a cero" in str(exc.value).lower()


# -- Caja: Egresos -----------------------------------------------------------------


def test_registrar_egreso_exitoso(db_session):
    data = transaccion_egreso_valida()
    transaccion = admin_service.registrar_egreso(db_session, data)

    assert transaccion.id is not None
    assert transaccion.tipo == "EGRESO"
    assert transaccion.monto == 200.0


def test_registrar_egreso_tipo_invalido(db_session):
    data = transaccion_egreso_valida()
    data.tipo = "INGRESO"

    with pytest.raises(ReglaNegocioError) as exc:
        admin_service.registrar_egreso(db_session, data)
    assert "debe ser egreso" in str(exc.value).lower()


def test_registrar_egreso_monto_negativo(db_session):
    data = transaccion_egreso_valida()
    data.monto = -10

    with pytest.raises(ReglaNegocioError) as exc:
        admin_service.registrar_egreso(db_session, data)
    assert "mayor a cero" in str(exc.value).lower()


# -- Reporte de ingresos -----------------------------------------------------------


def test_consultar_ingresos_por_fecha_exitoso(db_session):
    data = transaccion_ingreso_valida()
    admin_service.registrar_ingreso(db_session, data)

    resultado = admin_service.consultar_ingresos_por_fecha(
        db_session, date(2025, 1, 1), date(2025, 1, 31)
    )
    assert len(resultado) == 1
    assert resultado[0].monto == 500.0


def test_consultar_ingresos_por_fecha_fuera_rango(db_session):
    data = transaccion_ingreso_valida()
    admin_service.registrar_ingreso(db_session, data)

    resultado = admin_service.consultar_ingresos_por_fecha(
        db_session, date(2025, 2, 1), date(2025, 2, 28)
    )
    assert len(resultado) == 0


def test_consultar_ingresos_fecha_inicio_posterior_a_fin(db_session):
    with pytest.raises(ReglaNegocioError) as exc:
        admin_service.consultar_ingresos_por_fecha(
            db_session, date(2025, 6, 1), date(2025, 1, 1)
        )
    assert "posterior" in str(exc.value).lower()


def test_registrar_comprobante_crea_transaccion_caja(db_session):
    data = comprobante_valido()
    comprobante = admin_service.registrar_comprobante(db_session, data)

    ingresos = admin_service.consultar_ingresos_por_fecha(
        db_session, date(2025, 1, 1), date(2025, 1, 31)
    )

    assert any(t.comprobante_id == comprobante.id for t in ingresos)
