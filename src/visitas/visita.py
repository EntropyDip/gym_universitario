from dataclasses import dataclass
from .validaciones import es_fecha_valida

@dataclass
class Visita:
    documento: str
    horario: str
    duracion: int
    equipos: list[str]

    def __post_init__(self):
        if self.duracion <= 0:
            raise ValueError("La duración debe ser un número positivo de minutos")
        
        self.equipos = list(self.equipos)
        
        if not self.documento.strip():
            raise ValueError("El documento no puede estar vacío")

        # Integración con tus validaciones de fecha
        fecha_extraida = self.horario.split(" ")[0]  # Si el horario incluye la fecha (ej: "2026-10-19 10:00")
        if not es_fecha_valida(fecha_extraida):
            raise ValueError("La fecha del horario no es válida")