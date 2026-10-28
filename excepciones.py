"""Excepciones de negocio del gimnasio.

Toda regla violada lanza una excepción que hereda de GymError. La interfaz
captura GymError y muestra el mensaje en un cuadro de diálogo.
"""


class GymError(Exception):
    """Clase base de los errores de negocio del gimnasio."""


class DatoVacioError(GymError):
    """Un campo obligatorio llegó vacío."""


class FechaInvalidaError(GymError):
    """La fecha no tiene formato AAAA-MM-DD o no existe en el calendario."""


class DuracionInvalidaError(GymError):
    """La duración de la visita no es un entero mayor que cero."""


class UsuarioNoRegistradoError(GymError):
    """El documento no existe o el nombre no coincide con el registrado."""


class UsuarioYaRegistradoError(GymError):
    """Ya existe un usuario con ese documento."""


class HorarioInvalidoError(GymError):
    """El horario no está en la lista de horarios disponibles."""


class ReservaNoEncontradaError(GymError):
    """No existe una reserva con los datos indicados."""


class PrioridadNoEncontradaError(GymError):
    """No existe una prioridad con los datos indicados."""


class ReservaDuplicadaError(GymError):
    """El usuario ya tiene una reserva activa en esa fecha (o el cupo ya es suyo)."""


class CupoLlenoError(GymError):
    """La franja (fecha y horario) ya alcanzó el máximo de usuarios permitidos."""


class PrioridadNoCumpleError(GymError):
    """El usuario no cumple los requisitos para tener prioridad."""


class VisitaDuplicadaError(GymError):
    """El usuario ya tiene una visita registrada en esa fecha y horario."""


class CorreoInvalidoError(GymError):
    """El correo electrónico no tiene un formato válido."""


class DatosContactoRequeridosError(GymError):
    """La reserva necesita correo y celular que aún no están registrados."""


class PersistenciaError(GymError):
    """No se pudieron leer o guardar los datos persistidos."""
