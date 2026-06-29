import datetime
import pytest
from app.models.cita import Cita
from app.models.consulta_medica import ConsultaMedica
from app.models.prescripcion_medica import PrescripcionMedica


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


# COMMIT 2: PRUEBAS DE PRESCRIPCIÓN MÉDICA

def test_crear_prescripcion_medica_modelo(db_session, test_cita, test_paciente, test_medico):
    # Creamos una consulta médica real en la base de datos
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        diagnostico="Infección respiratoria"
    )
    db_session.add(consulta)
    db_session.commit()
    db_session.refresh(consulta)

    # Creamos la prescripción asociada a esa consulta
    prescripcion = PrescripcionMedica(
        consulta_id=consulta.id,
        medicamento="Amoxicilina 500mg",
        dosis="1 cápsula",
        frecuencia="Cada 8 horas",
        duracion="7 días",
        indicaciones="Tomar con abundantes líquidos después de las comidas"
    )
    db_session.add(prescripcion)
    db_session.commit()
    db_session.refresh(prescripcion)

    assert prescripcion.id is not None
    assert prescripcion.medicamento == "Amoxicilina 500mg"
    assert prescripcion.consulta_id == consulta.id

def test_verificar_relacion_consulta_prescripcion(db_session, test_cita, test_paciente, test_medico):
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        diagnostico="Dolor muscular"
    )
    db_session.add(consulta)
    db_session.commit()
    db_session.refresh(consulta)

    p1 = PrescripcionMedica(consulta_id=consulta.id, medicamento="Ibuprofeno 400mg", frecuencia="8 horas")
    p2 = PrescripcionMedica(consulta_id=consulta.id, medicamento="Paracetamol 500mg", frecuencia="6 horas")
    db_session.add_all([p1, p2])
    db_session.commit()

    # Refrescamos la consulta y verificamos que ORM cargue la lista de medicamentos automáticamente
    db_session.refresh(consulta)
    assert len(consulta.prescripciones) == 2
    assert consulta.prescripciones[0].medicamento in ["Ibuprofeno 400mg", "Paracetamol 500mg"]