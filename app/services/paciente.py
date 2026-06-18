from fastapi import HTTPException

from app.models.paciente import Paciente
from app.repositories.paciente_repository import PacienteRepository

class PacienteService:

    @staticmethod
    def crear_paciente(db, datos):

        if len(datos.cedula) != 10:
            raise HTTPException(
                status_code=400,
                detail="La cédula debe tener 10 dígitos"
            )

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
            nombres=datos.nombres,
            apellidos=datos.apellidos,
            cedula=datos.cedula,
            telefono=datos.telefono
        )

        return PacienteRepository.crear(db, paciente)