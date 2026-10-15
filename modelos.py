"""Entidades del gimnasio."""
from dataclasses import dataclass
from excepciones import DatoVacioError

@dataclass
class Usuario:
# Representa a un usuario del gimnasio y guarda sus datos personales y académicos.
    nombre: str
    documento: str
    programa: str

   def __post_init__(self):
        self.nombre = self.nombre.strip()
        self.documento = self.documento.strip()
        self.programa = self.programa.strip()
        if not self.nombre:
            raise DatoVacioError("El nombre no puede quedar vacío.")
        if not self.documento:
            raise DatoVacioError("El documento no puede estar vacío.")
        if not self.programa:
            raise DatoVacioError("El programa académico no puede quedar vacío.")
            raise DatoVacioError("el horario no puede quedar vacio")
