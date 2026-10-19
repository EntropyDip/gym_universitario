from .visita import Visita

class VisitaRepositorio:
    def __init__(self):
        self._visitas:list[str] = []

def guardar(self, visita: Visita) -> None:
        if not isinstance(visita, Visita):
            raise TypeError("Solo se pueden guardar instancias de Visita")
        self._visitas.append(visita)