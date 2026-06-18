from fastapi import HTTPException

from app.models.medico import Medico
from app.repositories.medico import MedicoRepository


class MedicoService:

    @staticmethod
    def crear_medico(db, datos):

        medico = Medico(
            nombres=datos.nombres,
            especialidad=datos.especialidad
        )

        return MedicoRepository.crear(
            db,
            medico
        )

    @staticmethod
    def listar_medicos(db):
        return MedicoRepository.obtener_todos(db)

    @staticmethod
    def obtener_medico(db, medico_id):

        medico = MedicoRepository.obtener_por_id(
            db,
            medico_id
        )

        if not medico:
            raise HTTPException(
                status_code=404,
                detail="Médico no encontrado"
            )

        return medico

    @staticmethod
    def actualizar_medico(
        db,
        medico_id,
        datos
    ):

        medico = MedicoRepository.obtener_por_id(
            db,
            medico_id
        )

        if not medico:
            raise HTTPException(
                status_code=404,
                detail="Médico no encontrado"
            )

        medico.nombres = datos.nombres
        medico.especialidad = datos.especialidad

        return MedicoRepository.actualizar(
            db,
            medico
        )

    @staticmethod
    def eliminar_medico(
        db,
        medico_id
    ):

        medico = MedicoRepository.obtener_por_id(
            db,
            medico_id
        )

        if not medico:
            raise HTTPException(
                status_code=404,
                detail="Médico no encontrado"
            )

        MedicoRepository.eliminar(
            db,
            medico
        )

        return {
            "mensaje": "Médico eliminado correctamente"
        }