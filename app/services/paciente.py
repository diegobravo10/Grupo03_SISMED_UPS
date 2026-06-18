from fastapi import HTTPException

from app.models.paciente import Paciente
from app.repositories.paciente import PacienteRepository


class PacienteService:

    @staticmethod
    def crear_paciente(db, datos):

        existente = PacienteRepository.obtener_por_cedula(
            db,
            datos.cedula
        )

        if existente:
            raise HTTPException(
                status_code=400,
                detail="La cédula ya existe"
            )

        paciente = Paciente(
            cedula=datos.cedula,
            nombres=datos.nombres,
            apellidos=datos.apellidos,
            telefono=datos.telefono
        )

        return PacienteRepository.crear(
            db,
            paciente
        )

    @staticmethod
    def listar_pacientes(db):
        return PacienteRepository.obtener_todos(db)

    @staticmethod
    def obtener_paciente(db, paciente_id):

        paciente = PacienteRepository.obtener_por_id(
            db,
            paciente_id
        )

        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        return paciente

    @staticmethod
    def actualizar_paciente(
        db,
        paciente_id,
        datos
    ):

        paciente = PacienteRepository.obtener_por_id(
            db,
            paciente_id
        )

        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        paciente.cedula = datos.cedula
        paciente.nombres = datos.nombres
        paciente.apellidos = datos.apellidos
        paciente.telefono = datos.telefono

        return PacienteRepository.actualizar(
            db,
            paciente
        )

    @staticmethod
    def eliminar_paciente(
        db,
        paciente_id
    ):

        paciente = PacienteRepository.obtener_por_id(
            db,
            paciente_id
        )

        if not paciente:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        PacienteRepository.eliminar(
            db,
            paciente
        )

        return {
            "mensaje": "Paciente eliminado correctamente"
        }