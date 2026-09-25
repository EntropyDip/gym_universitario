class GymError(Exception):
    """Excepción base para todos los errores del gimnasio."""
    pass


class DatoVacioError(GymError):
    """Se lanza cuando un campo obligatorio (nombre, documento, programa, horario) está vacío."""
    pass


class FechaInvalidaError(GymError):
    """Se lanza cuando una fecha no tiene el formato AAAA-MM-DD o no existe en el calendario."""
    pass


class DuracionInvalidaError(GymError):
    """Se lanza cuando la duración de una visita no es un número positivo de minutos."""
    pass


class UsuarioNoRegistradoError(GymError):
    """Se lanza cuando se intenta operar con un documento que no está registrado."""
    pass


class UsuarioYaRegistradoError(GymError):
    """Se lanza cuando se intenta registrar un documento que ya existe."""
    pass


class HorarioInvalidoError(GymError):
    """Se lanza cuando el horario solicitado no está entre los disponibles."""
    pass


class ReservaNoEncontradaError(GymError):
    """Se lanza cuando no se encuentra una reserva con los datos dados."""
    pass


class PrioridadNoEncontradaError(GymError):
    """Se lanza cuando no se encuentra una prioridad con los datos dados."""
    pass
