"""Reglas de negocio del gimnasio (GymService)."""
from excepciones import UsuarioNoRegistradoError, UsuarioYaRegistradoError
from modelos import Usuario
 
 
class GymService:
    """Aplica las reglas del gimnasio; es el Gym del código.
 
    Recibe los repositorios por inyección. visitas y prioridades son opcionales
    mientras los módulos de Juan José y Angelina no estén fusionados.
    """
 
    def __init__(self, usuarios, reservas, visitas=None, prioridades=None,
                 nombre: str = "Gimnasio universitario",
                 duracion_maxima_sesion: str = "1:30 horas") -> None:
        """Crea el servicio con sus repositorios y la configuración del gimnasio."""
        self.nombre = nombre
        self.horarios_disponibles: list[str] = ["08:00 AM", "10:00 AM", "02:00 PM"]
        self.duracion_maxima_sesion = duracion_maxima_sesion
        self.usuarios = usuarios
        self.reservas = reservas
        self.visitas = visitas
        self.prioridades = prioridades
