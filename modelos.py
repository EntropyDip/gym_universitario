from excepciones import DatoVacioError, FechaInvalidaError

@dataclass
class Reserva:
# Representa una reserva del gimnasio y almacena sus datos y estado.
    documento: str
    nombre_usuario: str
    horario: str
    fecha: str 
    activa: bool = True

    def __post_init__(self):
        self.documento = self.documento.strip()
        self.nombre_usuario = self.nombre_usuario.strip()
        self.horario = self.horario.strip()
        self.fecha = self.fecha.strip()
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
        return self.documento == documento
 
    def mostrar_resumen(self) -> str:
        """Devuelve el resumen de la reserva: usuario, documento, fecha, horario y estado."""
        estado = "activa" if self.activa else "cancelada"
        return (f"Reserva ({estado}) — {self.nombre_usuario} ({self.documento}), "
                f"{self.fecha}, {self.horario}.")
            
