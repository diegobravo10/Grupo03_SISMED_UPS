from app.schemas.medico import MedicoCreate
from app.services.medico import MedicoService


def test_crear_medico_exitoso(db_session):
    datos = MedicoCreate(
        nombres="Ana",
        especialidad="Pediatría"
    )

    medico = MedicoService.crear_medico(db_session, datos)

    assert medico.id is not None
    assert medico.nombres == "Ana"
    assert medico.especialidad == "Pediatría"


def test_buscar_medico_por_id(db_session):
    datos = MedicoCreate(
        nombres="Ana",
        especialidad="Pediatría"
    )

    creado = MedicoService.crear_medico(db_session, datos)
    medico = MedicoService.obtener_medico(db_session, creado.id)

    assert medico.id == creado.id
    assert medico.nombres == "Ana"
    assert medico.especialidad == "Pediatría"


def test_listar_medicos(db_session):
    datos = MedicoCreate(
        nombres="Ana",
        especialidad="Pediatría"
    )

    MedicoService.crear_medico(db_session, datos)
    medicos = MedicoService.listar_medicos(db_session)

    assert len(medicos) == 1
    assert medicos[0].nombres == "Ana"


def test_actualizar_medico(db_session):
    datos = MedicoCreate(
        nombres="Ana",
        especialidad="Pediatría"
    )

    creado = MedicoService.crear_medico(db_session, datos)

    datos_actualizados = MedicoCreate(
        nombres="Ana María",
        especialidad="Medicina General"
    )

    actualizado = MedicoService.actualizar_medico(
        db_session,
        creado.id,
        datos_actualizados
    )

    assert actualizado.id == creado.id
    assert actualizado.nombres == "Ana María"
    assert actualizado.especialidad == "Medicina General"
