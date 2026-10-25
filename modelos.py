"""Entidades del gimnasio y utilidades de fecha."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from excepciones import (
    DatoVacioError,
    DuracionInvalidaError,
    FechaInvalidaError,
)      

# ------------------------------------------------------------------ Utilidades de fecha (Juan José)









# ------------------------------------------------------------------ Entidades (Samuel)
@dataclass
class Usuario:
    """Representa a un estudiante o usuario del gimnasio."""
    nombre: str
    documento: str
    programa: str

    def __post_init__(self) -> None:
        self.nombre = str(self.nombre).strip()
        self.documento = str(self.documento).strip()
        self.programa = str(self.programa).strip()
        if not self.nombre:
            raise DatoVacioError("El nombre no puede quedar vacío.")
        if not self.documento:
            raise DatoVacioError("El documento no puede estar vacío.")
        if not self.programa:
            raise DatoVacioError("El programa académico no puede quedar vacío.")


@dataclass
class Reserva:
    """Representa el apartado de un horario por parte de un usuario."""
    documento: str
    nombre_usuario: str
    horario: str
    fecha: str
    activa: bool = True

    def __post_init__(self) -> None:
        self.documento = str(self.documento).strip()
        self.nombre_usuario = str(self.nombre_usuario).strip()
        self.horario = str(self.horario).strip()
        self.fecha = str(self.fecha).strip()
        if not self.documento:
            raise DatoVacioError("El documento no puede estar vacío.")
        if not self.nombre_usuario:
            raise DatoVacioError("El nombre de usuario no puede estar vacío.")
        if not self.horario:
            raise DatoVacioError("El horario no puede quedar vacío.")
        if not es_fecha_valida(self.fecha):
            raise FechaInvalidaError(
                "La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15.")

    def cancelar(self) -> str:
        """Cancela la reserva si estaba activa; si ya estaba cancelada, solo lo informa."""
        if not self.activa:
            return f"La reserva de {self.nombre_usuario} ya estaba cancelada."
        self.activa = False
        return f"Reserva de {self.nombre_usuario} a las {self.horario} cancelada."

    def confirmar(self) -> str:
        """Reactiva la reserva si estaba cancelada; si ya estaba activa, solo lo informa."""
        if self.activa:
            return f"La reserva de {self.nombre_usuario} ya está activa."
        self.activa = True
        return (f"Reserva de {self.nombre_usuario} confirmada nuevamente "
                f"para las {self.horario}.")

    def coincide_con(self, documento: str) -> bool:
        """Indica si la reserva pertenece al documento indicado."""
        return self.documento == documento.strip()

    def mostrar_resumen(self) -> str:
        """Devuelve el resumen de la reserva: usuario, documento, fecha, horario y estado."""
        estado = "activa" if self.activa else "cancelada"
        return (f"Reserva ({estado}) — {self.nombre_usuario} ({self.documento}), "
                f"{self.fecha}, {self.horario}.")


# ------------------------------------------------------------------ Entidad Visita (Juan José)










# ------------------------------------------------------------------ Entidad Prioridad (Angelina)










