from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401 - registra los modelos en Base.metadata
from app.database import Base, get_db
from app.main import app
from app.models.medico import Medico
from app.models.paciente import Paciente


TEST_DATABASE_URL = f"sqlite:///{Path(__file__).parent / 'test_sismed.db'}"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(autouse=True)
def reset_tables():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def test_paciente(db_session):
    paciente = Paciente(
        cedula="0102030405",
        nombres="Paciente",
        apellidos="Prueba",
        telefono="0999999999",
    )
    db_session.add(paciente)
    db_session.commit()
    db_session.refresh(paciente)
    return paciente


@pytest.fixture
def test_medico(db_session):
    medico = Medico(
        nombres="Medico Prueba",
        especialidad="Medicina General",
    )
    db_session.add(medico)
    db_session.commit()
    db_session.refresh(medico)
    return medico
