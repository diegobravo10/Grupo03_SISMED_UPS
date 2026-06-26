from app.models.medico import Medico


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


def test_no_permite_crear_cita_con_paciente_inexistente(
    client, test_paciente, test_medico
):
    payload = cita_payload(test_paciente, test_medico)
    payload["paciente_id"] = 9999

    response = client.post("/citas/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Paciente no encontrado"


def test_no_permite_crear_cita_con_medico_inexistente(
    client, test_paciente, test_medico
):
    payload = cita_payload(test_paciente, test_medico)
    payload["medico_id"] = 9999

    response = client.post("/citas/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Médico no encontrado"


def test_no_permite_crear_cita_con_hora_inicio_mayor_o_igual_que_hora_fin(
    client, test_paciente, test_medico
):
    payload = cita_payload(test_paciente, test_medico)
    payload["hora_inicio"] = "09:30:00"
    payload["hora_fin"] = "09:30:00"

    response = client.post("/citas/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "La hora de inicio debe ser anterior a la hora de fin"


def test_no_permite_crear_cita_con_cruce_de_horario_para_mismo_medico(
    client, test_paciente, test_medico
):
    crear_cita(client, test_paciente, test_medico)
    payload = cita_payload(test_paciente, test_medico)
    payload["hora_inicio"] = "09:15:00"
    payload["hora_fin"] = "09:45:00"

    response = client.post("/citas/", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "El médico ya tiene una cita registrada en ese horario"


def test_permite_cita_en_mismo_horario_si_es_otro_medico(
    client, db_session, test_paciente, test_medico
):
    crear_cita(client, test_paciente, test_medico)
    otro_medico = Medico(nombres="Otro Medico", especialidad="Pediatria")
    db_session.add(otro_medico)
    db_session.commit()
    db_session.refresh(otro_medico)
    payload = cita_payload(test_paciente, test_medico)
    payload["medico_id"] = otro_medico.id

    response = client.post("/citas/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["medico_id"] == otro_medico.id
    assert data["hora_inicio"] == "09:00:00"
    assert data["hora_fin"] == "09:30:00"


def test_permite_cita_del_mismo_medico_en_horario_diferente(
    client, test_paciente, test_medico
):
    crear_cita(client, test_paciente, test_medico)
    payload = cita_payload(test_paciente, test_medico)
    payload["hora_inicio"] = "10:00:00"
    payload["hora_fin"] = "10:30:00"

    response = client.post("/citas/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["medico_id"] == test_medico.id
    assert data["hora_inicio"] == "10:00:00"
    assert data["hora_fin"] == "10:30:00"
