class EntidadNoEncontradaError(Exception):
    """Se lanza cuando una entidad (paciente, médico, cita) no existe."""


class ReglaNegocioError(Exception):
    """Se lanza cuando se viola una regla de negocio (cruce de horario, estado inválido, etc.)."""
