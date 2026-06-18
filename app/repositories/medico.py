from app.models.medico import Medico


class MedicoRepository:

    @staticmethod
    def obtener_todos(db):
        return db.query(Medico).all()

    @staticmethod
    def obtener_por_id(db, medico_id):
        return db.query(Medico).filter(
            Medico.id == medico_id
        ).first()

    @staticmethod
    def crear(db, medico):
        db.add(medico)
        db.commit()
        db.refresh(medico)
        return medico

    @staticmethod
    def actualizar(db, medico):
        db.commit()
        db.refresh(medico)
        return medico

    @staticmethod
    def eliminar(db, medico):
        db.delete(medico)
        db.commit()