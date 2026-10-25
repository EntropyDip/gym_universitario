
from .src import Visita
def registrar_visita(self, documento: str, horario: str, duracion: int, equipos: list[str]) -> str:
        doc_limpio = str(documento).strip()
        usuario = self._exigir_usuario(doc_limpio)
        self._validar_horario(horario)
        nueva_visita = Visita(doc_limpio, horario, duracion, equipos)
        if self.visitas is not None:
            self.visitas.agregar(nueva_visita)
        return f"Visita de {usuario.nombre} registrada correctamente."

def listar_visitas(self) -> list[Visita]:
        """Devuelve la lista de visitas registradas."""
        if self.visitas is None:
            return []
        return self.visitas.listar()

def horario_mas_frecuente(self) -> str:
        """Calcula el horario con mayor afluencia de visitas registradas (R5)."""
        visitas = self.listar_visitas()
        if not visitas:
            return "No hay visitas registradas."

        conteo: dict[str, int] = {}
        for v in visitas:
            conteo[v.horario] = conteo.get(v.horario, 0) + 1

        horario_top = max(conteo, key=conteo.get)
        return f"El horario más frecuente es {horario_top}."

def programa_mas_frecuente(self) -> str:
        """Calcula la carrera o programa con mayor cantidad de usuarios registrados (R6)."""
        usuarios = self.listar_usuarios()
        if not usuarios:
            return "No hay usuarios registrados."

        conteo: dict[str, int] = {}
        for u in usuarios:
            conteo[u.programa] = conteo.get(u.programa, 0) + 1

        programa_top = max(conteo, key=conteo.get)
        return f"La carrera más frecuente es {programa_top}."

def promedio_duracion_por_usuario(self) -> str:
        """Genera un informe textual con el tiempo promedio en minutos por usuario (R11)."""
        datos = self.datos_promedio_duracion()
        if not datos:
            return "No hay visitas registradas."

        lineas = ["Promedio de duración por usuario:"]
        for nombre, promedio in datos:
            lineas.append(f"- {nombre}: {promedio:.1f} minutos en promedio")
        return "\n".join(lineas)