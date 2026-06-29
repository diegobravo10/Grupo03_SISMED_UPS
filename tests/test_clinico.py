import datetime
import pytest
from app.models.cita import Cita
from app.models.consulta_medica import ConsultaMedica


@pytest.fixture
def test_cita(db_session, test_paciente, test_medico):
    cita = Cita(
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        fecha=datetime.date(2026, 6, 29),
        hora_inicio=datetime.time(10, 0),
        hora_fin=datetime.time(10, 30),
        motivo="Consulta clínica obligatoria",
        estado="ATENDIDA"
    )
    db_session.add(cita)
    db_session.commit()
    db_session.refresh(cita)
    return cita

# COMMIT 1: PRUEBAS DE CONSULTA MÉDICA
def test_crear_consulta_medica_modelo(db_session, test_cita, test_paciente, test_medico):
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        motivo="Dolor abdominal agudo",
        anamnesis="Paciente refiere dolor de 12 horas de evolución",
        diagnostico="Gastritis aguda",
        observaciones="Tomar líquidos con frecuencia",
        tratamiento="Omeprazol 20mg en ayunas"
    )
    db_session.add(consulta)
    db_session.commit()
    db_session.refresh(consulta)

    assert consulta.id is not None
    assert consulta.diagnostico == "Gastritis aguda"
    assert consulta.cita_id == test_cita.id

def test_verificar_relaciones_consulta(db_session, test_cita, test_paciente, test_medico):
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        diagnostico="Chequeo rutinario"
    )
    db_session.add(consulta)
    db_session.commit()

    # Validamos que el ORM conecte las tablas de forma automática
    assert consulta.paciente.cedula == test_paciente.cedula
    assert consulta.medico.nombres == test_medico.nombres