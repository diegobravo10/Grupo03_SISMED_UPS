from app.models.paciente import Paciente

class PacienteRepository:

    @staticmethod
    def obtener_todos(db):
        return db.query(Paciente).all()

    @staticmethod
    def obtener_por_id(db, paciente_id):
        return db.query(Paciente).filter(
            Paciente.id == paciente_id
        ).first()

    @staticmethod
    def obtener_por_cedula(db, cedula):
        return db.query(Paciente).filter(
            Paciente.cedula == cedula
        ).first()

    @staticmethod
    def crear(db, paciente):
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        return paciente