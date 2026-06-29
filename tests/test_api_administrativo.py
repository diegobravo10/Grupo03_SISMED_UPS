from datetime import date

from app.schemas.comprobante_venta import ComprobanteVentaCreate
from app.schemas.transaccion_caja import TransaccionCajaCreate


COMPROBANTE_PAYLOAD = {
    "tipo_comprobante": "FACTURA",
    "serie": "F001",
    "numero": "00000001",
    "cliente_nombre": "Empresa SAC",
    "cliente_documento": "20123456789",
    "fecha_emision": "2025-01-15",
    "subtotal": 200.0,
    "igv": 36.0,
    "total": 236.0,
}


def test_post_comprobante_201(client):
    resp = client.post("/admin/comprobantes/", json=COMPROBANTE_PAYLOAD)
    assert resp.status_code == 201
    data = resp.json()
    assert data["tipo_comprobante"] == "FACTURA"
    assert data["total"] == 236.0
    assert "id" in data


def test_post_comprobante_total_invalido_400(client):
    payload = {**COMPROBANTE_PAYLOAD, "total": 999.0}
    resp = client.post("/admin/comprobantes/", json=payload)
    assert resp.status_code == 400


def test_get_comprobantes(client):
    client.post("/admin/comprobantes/", json=COMPROBANTE_PAYLOAD)
    resp = client.get("/admin/comprobantes/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["serie"] == "F001"


def test_post_ingreso_201(client):
    payload = {
        "tipo": "INGRESO",
        "concepto": "Venta mostrador",
        "monto": 350.0,
        "fecha": "2025-01-15",
    }
    resp = client.post("/admin/caja/ingresos", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["tipo"] == "INGRESO"
    assert data["monto"] == 350.0


def test_post_ingreso_tipo_invalido_400(client):
    payload = {
        "tipo": "EGRESO",
        "concepto": "Venta mostrador",
        "monto": 350.0,
        "fecha": "2025-01-15",
    }
    resp = client.post("/admin/caja/ingresos", json=payload)
    assert resp.status_code == 400


def test_post_egreso_201(client):
    payload = {
        "tipo": "EGRESO",
        "concepto": "Pago luz",
        "monto": 150.0,
        "fecha": "2025-01-15",
    }
    resp = client.post("/admin/caja/egresos", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["tipo"] == "EGRESO"


def test_post_egreso_tipo_invalido_400(client):
    payload = {
        "tipo": "INGRESO",
        "concepto": "Pago luz",
        "monto": 150.0,
        "fecha": "2025-01-15",
    }
    resp = client.post("/admin/caja/egresos", json=payload)
    assert resp.status_code == 400


def test_get_ingresos_por_fecha(client):
    client.post("/admin/caja/ingresos", json={
        "tipo": "INGRESO",
        "concepto": "Venta A",
        "monto": 100.0,
        "fecha": "2025-01-15",
    })
    client.post("/admin/caja/ingresos", json={
        "tipo": "INGRESO",
        "concepto": "Venta B",
        "monto": 200.0,
        "fecha": "2025-01-20",
    })

    resp = client.get(
        "/admin/caja/ingresos",
        params={"fecha_inicio": "2025-01-01", "fecha_fin": "2025-01-31"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


def test_get_ingresos_fecha_invalida_400(client):
    resp = client.get(
        "/admin/caja/ingresos",
        params={"fecha_inicio": "2025-06-01", "fecha_fin": "2025-01-01"},
    )
    assert resp.status_code == 400


def test_post_comprobante_crea_transaccion_caja(client):
    client.post("/admin/comprobantes/", json=COMPROBANTE_PAYLOAD)

    resp = client.get(
        "/admin/caja/ingresos",
        params={"fecha_inicio": "2025-01-01", "fecha_fin": "2025-01-31"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["concepto"].startswith("Venta")
