import datetime
import pytest
from app.models.cita import Cita
from app.models.consulta_medica import ConsultaMedica
from app.models.prescripcion_medica import PrescripcionMedica
from app.models.orden_medica import OrdenMedica
from app.models.certificado_medico import CertificadoMedico


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

# COMMIT 3: PRUEBAS DE ÓRDENES MÉDICAS

def test_crear_orden_medica_modelo(db_session, test_cita, test_paciente, test_medico):
    # Creamos la consulta médica base
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        diagnostico="Sospecha de apendicitis aguda"
    )
    db_session.add(consulta)
    db_session.commit()
    db_session.refresh(consulta)

    # Creamos la orden 
    orden = OrdenMedica(
        consulta_id=consulta.id,
        tipo="Laboratorio",
        descripcion="Biometría hemática completa",
        indicaciones="Presentarse en ayuno estricto de 8 horas"
    )
    db_session.add(orden)
    db_session.commit()
    db_session.refresh(orden)

    assert orden.id is not None
    assert orden.tipo == "Laboratorio"
    assert orden.consulta_id == consulta.id

def test_verificar_relacion_consulta_ordenes(db_session, test_cita, test_paciente, test_medico):
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        diagnostico="Traumatismo de rodilla derecha"
    )
    db_session.add(consulta)
    db_session.commit()
    db_session.refresh(consulta)

    # Generamos dos órdenes distintas para la misma consulta
    o1 = OrdenMedica(consulta_id=consulta.id, tipo="Imagenología", descripcion="Rayos X de rodilla AP y Lateral")
    o2 = OrdenMedica(consulta_id=consulta.id, tipo="Laboratorio", descripcion="Ácido úrico en sangre")
    
    db_session.add_all([o1, o2])
    db_session.commit()

    db_session.refresh(consulta)
    
    assert len(consulta.ordenes) == 2
    tipos_generados = [o.tipo for o in consulta.ordenes]
    assert "Imagenología" in tipos_generados
    assert "Laboratorio" in tipos_generados

# COMMIT 4: PRUEBAS DE CERTIFICADOS MÉDICOS

def test_crear_certificado_medico_modelo(db_session, test_cita, test_paciente, test_medico):
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        diagnostico="Lumbalgia aguda post-esfuerzo"
    )
    db_session.add(consulta)
    db_session.commit()
    db_session.refresh(consulta)

    certificado = CertificadoMedico(
        consulta_id=consulta.id,
        tipo="Reposo Médico",
        contenido="Se concede reposo médico absoluto por el lapso de 72 horas a partir de la fecha."
    )
    db_session.add(certificado)
    db_session.commit()
    db_session.refresh(certificado)

    assert certificado.id is not None
    assert certificado.tipo == "Reposo Médico"
    assert "72 horas" in certificado.contenido

def test_verificar_relacion_consulta_certificados(db_session, test_cita, test_paciente, test_medico):
    consulta = ConsultaMedica(
        cita_id=test_cita.id,
        paciente_id=test_paciente.id,
        medico_id=test_medico.id,
        diagnostico="Control de salud ocupacional"
    )
    db_session.add(consulta)
    db_session.commit()
    db_session.refresh(consulta)

    c1 = CertificadoMedico(consulta_id=consulta.id, tipo="Asistencia", contenido="Paciente asistió a consulta médica.")
    c2 = CertificadoMedico(consulta_id=consulta.id, tipo="Aptitud", contenido="Apto para realizar actividades físicas.")
    
    db_session.add_all([c1, c2])
    db_session.commit()

    db_session.refresh(consulta)
    assert len(consulta.certificados) == 2