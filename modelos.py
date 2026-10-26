"""Entidades del gimnasio y utilidades de fecha."""
from dataclasses import dataclass
from datetime import datetime, timedelta

from excepciones import (
    DatoVacioError,
    DuracionInvalidaError,
    FechaInvalidaError,
)      

# ------------------------------------------------------------------ Utilidades de fecha (Juan José)

def es_bisiesto(anio: int) -> bool:
    """Determina si un año es bisiesto según las reglas gregorianas."""
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def es_fecha_valida(fecha: str) -> bool:
    """Valida matemáticamente que la fecha tenga formato AAAA-MM-DD y exista en el calendario."""
    if not isinstance(fecha, str):
        return False
    partes = fecha.strip().split("-")
    if len(partes) != 3:
        return False

    anio_texto, mes_texto, dia_texto = partes
    if not (anio_texto.isdigit() and mes_texto.isdigit() and dia_texto.isdigit()):
        return False
    if len(anio_texto) != 4 or len(mes_texto) != 2 or len(dia_texto) != 2:
        return False

    anio, mes, dia = int(anio_texto), int(mes_texto), int(dia_texto)
    if not 1 <= mes <= 12:
        return False

    dias_por_mes = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    maximo_dia = dias_por_mes[mes - 1]
    if mes == 2 and not es_bisiesto(anio):
        maximo_dia = 28

    return 1 <= dia <= maximo_dia

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

@dataclass
class Visita:
    """Registra la asistencia efectiva de un usuario al gimnasio y los equipos utilizados."""
    documento: str
    horario: str
    duracion: int
    equipos: list[str]
    fecha: str

    def __post_init__(self) -> None:
        self.documento = str(self.documento).strip()
        self.horario = str(self.horario).strip()
        if not self.documento:
            raise DatoVacioError("El documento no puede estar vacío.")
        if not self.horario:
            raise DatoVacioError("El horario no puede quedar vacío.")
        self.fecha = str(self.fecha).strip()
        if not self.fecha:
            raise DatoVacioError("La fecha de la visita no puede quedar vacía.")
        if not es_fecha_valida(self.fecha):
            raise FechaInvalidaError(
                "La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15.")
        # Excluir booleanos (que en Python heredan de int) y validar entero positivo
        if isinstance(self.duracion, bool) or not isinstance(self.duracion, int) or self.duracion <= 0:
            raise DuracionInvalidaError("La duración debe ser un número entero positivo de minutos.")

        # Limpiar equipos
        equipos_limpios = []
        for eq in self.equipos:
            limpio = str(eq).strip()
            if limpio:
                equipos_limpios.append(limpio)
        self.equipos = equipos_limpios

# ------------------------------------------------------------------ Entidad Prioridad (Angelina)

@dataclass
class Prioridad:
    """Representa un cupo apartado con prioridad de membresía para un usuario."""
    documento: str
    nombre: str
    horario: str
    fecha: str
    hora_solicitud: datetime
    confirmada: bool = False

    def __post_init__(self) -> None:
        self.documento = str(self.documento).strip()
        self.nombre = str(self.nombre).strip()
        self.horario = str(self.horario).strip()
        self.fecha = str(self.fecha).strip()
        if not self.documento:
            raise DatoVacioError("El documento no puede estar vacío.")
        if not self.nombre:
            raise DatoVacioError("El nombre no puede quedar vacío.")
        if not self.horario:
            raise DatoVacioError("El horario no puede quedar vacío.")
        if not es_fecha_valida(self.fecha):
            raise FechaInvalidaError(
                "La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15.")

    def hora_del_horario(self) -> datetime:
        """Convierte la fecha y horario en un objeto datetime."""
        return datetime.strptime(f"{self.fecha} {self.horario}", "%Y-%m-%d %I:%M %p")

    def limite_confirmacion(self) -> datetime:
        """Calcula el límite estricto de confirmación (2 horas antes del horario apartado)."""
        return self.hora_del_horario() - timedelta(hours=2)

    def esta_vencida(self, hora_actual: datetime) -> bool:
        """Determina si la prioridad caducó por no haber sido confirmada a tiempo."""
        if self.confirmada:
            return False
        return hora_actual > self.limite_confirmacion()

    def confirmar(self) -> None:
        """Marca la prioridad como confirmada."""
        self.confirmada = True

