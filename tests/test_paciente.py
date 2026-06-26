import pytest
from fastapi import HTTPException

from app.schemas.paciente import PacienteCreate
from app.services.paciente import PacienteService


def test_crear_paciente_exitoso(db_session):
    datos = PacienteCreate(
        cedula="0102030405",
        nombres="Juan",
        apellidos="Pérez",
        telefono="0999999999"
    )

    paciente = PacienteService.crear_paciente(db_session, datos)

    assert paciente.id is not None
    assert paciente.cedula == "0102030405"
    assert paciente.nombres == "Juan"
    assert paciente.apellidos == "Pérez"
    assert paciente.telefono == "0999999999"


def test_crear_paciente_cedula_duplicada(db_session):
    datos = PacienteCreate(
        cedula="0102030405",
        nombres="Juan",
        apellidos="Pérez",
        telefono="0999999999"
    )

    PacienteService.crear_paciente(db_session, datos)

    with pytest.raises(HTTPException) as exc_info:
        PacienteService.crear_paciente(db_session, datos)

    assert exc_info.value.status_code == 400
    assert "cédula ya existe" in exc_info.value.detail


def test_buscar_paciente_por_id(db_session):
    datos = PacienteCreate(
        cedula="0102030405",
        nombres="Juan",
        apellidos="Pérez",
        telefono="0999999999"
    )

    creado = PacienteService.crear_paciente(db_session, datos)
    paciente = PacienteService.obtener_paciente(db_session, creado.id)

    assert paciente.id == creado.id
    assert paciente.cedula == "0102030405"
    assert paciente.nombres == "Juan"


def test_actualizar_paciente(db_session):
    datos = PacienteCreate(
        cedula="0102030405",
        nombres="Juan",
        apellidos="Pérez",
        telefono="0999999999"
    )

    creado = PacienteService.crear_paciente(db_session, datos)

    datos_actualizados = PacienteCreate(
        cedula="0102030405",
        nombres="Juan Carlos",
        apellidos="Pérez Gómez",
        telefono="0988887777"
    )

    actualizado = PacienteService.actualizar_paciente(
        db_session,
        creado.id,
        datos_actualizados
    )

    assert actualizado.id == creado.id
    assert actualizado.nombres == "Juan Carlos"
    assert actualizado.apellidos == "Pérez Gómez"
    assert actualizado.telefono == "0988887777"
