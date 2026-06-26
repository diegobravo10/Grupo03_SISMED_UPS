def cita_payload(test_paciente, test_medico):
    return {
        "paciente_id": test_paciente.id,
        "medico_id": test_medico.id,
        "fecha": "2026-07-01",
        "hora_inicio": "09:00:00",
        "hora_fin": "09:30:00",
        "motivo": "Consulta general",
    }


def crear_cita(client, test_paciente, test_medico):
    response = client.post("/citas/", json=cita_payload(test_paciente, test_medico))
    assert response.status_code == 201
    return response.json()


def test_crear_cita_correctamente(client, test_paciente, test_medico):
    data = crear_cita(client, test_paciente, test_medico)

    assert data["id"] is not None
    assert data["paciente_id"] == test_paciente.id
    assert data["medico_id"] == test_medico.id
    assert data["fecha"] == "2026-07-01"
    assert data["hora_inicio"] == "09:00:00"
    assert data["hora_fin"] == "09:30:00"
    assert data["motivo"] == "Consulta general"


def test_cita_creada_tiene_estado_separada(client, test_paciente, test_medico):
    data = crear_cita(client, test_paciente, test_medico)

    assert data["estado"] == "SEPARADA"


def test_listar_citas(client, test_paciente, test_medico):
    cita = crear_cita(client, test_paciente, test_medico)

    response = client.get("/citas/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == cita["id"]


def test_buscar_cita_por_id(client, test_paciente, test_medico):
    cita = crear_cita(client, test_paciente, test_medico)

    response = client.get(f"/citas/{cita['id']}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cita["id"]
    assert data["paciente_id"] == test_paciente.id
    assert data["medico_id"] == test_medico.id


def test_buscar_citas_por_medico(client, test_paciente, test_medico):
    cita = crear_cita(client, test_paciente, test_medico)

    response = client.get(f"/citas/medico/{test_medico.id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == cita["id"]
    assert data[0]["medico_id"] == test_medico.id


def test_buscar_citas_por_paciente(client, test_paciente, test_medico):
    cita = crear_cita(client, test_paciente, test_medico)

    response = client.get(f"/citas/paciente/{test_paciente.id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == cita["id"]
    assert data[0]["paciente_id"] == test_paciente.id
