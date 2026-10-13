from dataclasses import dataclass
from excepciones import DatoVacioError, FechaInvalidaError

# TODO: pendiente es_fecha_valida de Juan José

@dataclass
class Usuario:
# Representa a un usuario del gimnasio y guarda sus datos personales y académicos.
    nombre: str
    documento: str
    programa: str

    def __post_init__(self):
        if not self.nombre.strip():
            raise DatoVacioError("El nombre no puede quedar vacío")
        if not self.documento.strip():
            raise DatoVacioError("El documento no puede estar vacío")
        if not self.programa.strip():
            raise DatoVacioError("El programa académico no puede quedar vacío")

@dataclass
class Reserva:
# Representa una reserva del gimnasio y almacena sus datos y estado.
    documento: str
    nombre_usuario: str
    horario: str
    fecha: str 
    activa: bool = True

    def __post_init__(self):
        if not self.documento.strip():
            raise DatoVacioError("El documento no puede estar vacío")
        if not es_fecha_valida(self.fecha):
            raise FechaInvalidadError("La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15")
        if not self.nombre_usuario.strip():
            raise DatoVacioError("El nombre de usuario no puede estar vacío")
        if not self.horario.strip():
            raise DatoVacioError("el horario no puede quedar vacio")
