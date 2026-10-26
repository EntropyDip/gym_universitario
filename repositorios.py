"""Repositorios: interfaces abstractas e implementaciones en memoria."""
from abc import ABC, abstractmethod

from modelos import Prioridad, Reserva, Usuario, Visita

# ------------------------------------------------------------------ Repositorio de Usuarios (Samuel)
class UsuarioRepositorio(ABC):
    """Contrato abstracto para el almacenamiento de usuarios."""

    @abstractmethod
    def agregar(self, usuario: Usuario) -> None:
        """Guarda un nuevo usuario."""

    @abstractmethod
    def buscar(self, documento: str) -> Usuario | None:
        """Devuelve el usuario por documento o None si no existe."""

    @abstractmethod
    def listar(self) -> list[Usuario]:
        """Devuelve la lista de todos los usuarios registrados."""

    @abstractmethod
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina el usuario correspondiente al documento."""


class UsuarioRepositorioMemoria(UsuarioRepositorio):
    """Implementación en memoria del repositorio de usuarios."""

    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}

    def agregar(self, usuario: Usuario) -> None:
        self._usuarios[usuario.documento] = usuario

    def buscar(self, documento: str) -> Usuario | None:
        return self._usuarios.get(documento.strip())

    def listar(self) -> list[Usuario]:
        return list(self._usuarios.values())

    def eliminar_por_documento(self, documento: str) -> None:
        self._usuarios.pop(documento.strip(), None)

# ------------------------------------------------------------------ Repositorio de Reservas (Samuel)
class ReservaRepositorio(ABC):
    """Contrato abstracto para el almacenamiento de reservas."""

    @abstractmethod
    def agregar(self, reserva: Reserva) -> None:
        """Guarda una nueva reserva."""

    @abstractmethod
    def buscar(self, documento: str, horario: str, fecha: str,
               activa: bool | None = None) -> Reserva | None:
        """Busca una reserva específica con filtro opcional de estado."""

    @abstractmethod
    def buscar_por_documento(self, documento: str) -> list[Reserva]:
        """Obtiene todas las reservas asociadas a un documento."""

    @abstractmethod
    def listar(self) -> list[Reserva]:
        """Devuelve una copia de la lista de reservas."""

    @abstractmethod
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina todas las reservas asociadas al documento."""


class ReservaRepositorioMemoria(ReservaRepositorio):
    """Implementación en memoria del repositorio de reservas."""

    def __init__(self) -> None:
        self._reservas: list[Reserva] = []

    def agregar(self, reserva: Reserva) -> None:
        self._reservas.append(reserva)

    def buscar(self, documento: str, horario: str, fecha: str, activa: bool | None = None) -> Reserva | None:
        doc = documento.strip()
        for reserva in self._reservas:
            if (reserva.documento == doc and reserva.horario == horario
                    and reserva.fecha == fecha
                    and (activa is None or reserva.activa == activa)):
                return reserva
        return None

    def buscar_por_documento(self, documento: str) -> list[Reserva]:
        doc = documento.strip()
        return [r for r in self._reservas if r.documento == doc]

    def listar(self) -> list[Reserva]:
        return list(self._reservas)

    def eliminar_por_documento(self, documento: str) -> None:
        doc = documento.strip()
        self._reservas = [r for r in self._reservas if r.documento != doc]

# ------------------------------------------------------------------ Repositorio de Visitas (Juan José)

class VisitaRepositorio(ABC):
    """Contrato abstracto para el almacenamiento de visitas."""

    @abstractmethod
    def agregar(self, visita: Visita) -> None:
        """Guarda un registro de visita."""

    @abstractmethod
    def buscar_por_documento(self, documento: str) -> list[Visita]:
        """Retorna todas las visitas asociadas a un documento."""

    @abstractmethod
    def listar(self) -> list[Visita]:
        """Devuelve la lista completa de visitas."""

    @abstractmethod
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina todas las visitas de un usuario por documento."""


class VisitaRepositorioMemoria(VisitaRepositorio):
    """Implementación en memoria del repositorio de visitas."""

    def __init__(self) -> None:
        self._visitas: list[Visita] = []

    def agregar(self, visita: Visita) -> None:
        self._visitas.append(visita)

    def buscar_por_documento(self, documento: str) -> list[Visita]:
        doc = documento.strip()
        return [v for v in self._visitas if v.documento == doc]

    def listar(self) -> list[Visita]:
        return list(self._visitas)

    def eliminar_por_documento(self, documento: str) -> None:
        doc = documento.strip()
        self._visitas = [v for v in self._visitas if v.documento != doc]

# ------------------------------------------------------------------ Repositorio de Prioridades (Angelina)

class PrioridadRepositorio(ABC):
    """Contrato abstracto para el almacenamiento de prioridades."""

    @abstractmethod
    def agregar(self, prioridad: Prioridad) -> None:
        """Guarda una prioridad otorgada."""

    @abstractmethod
    def buscar(self, documento: str, horario: str, fecha: str) -> Prioridad | None:
        """Busca una prioridad por documento, horario y fecha."""

    @abstractmethod
    def buscar_por_cupo(self, horario: str, fecha: str) -> Prioridad | None:
        """Busca si un horario y fecha están apartados con prioridad."""

    @abstractmethod
    def listar(self) -> list[Prioridad]:
        """Lista todas las prioridades registradas."""

    @abstractmethod
    def eliminar(self, prioridad: Prioridad) -> None:
        """Elimina una prioridad específica."""
        
    @abstractmethod
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina todas las prioridades pertenecientes al documento."""

class PrioridadRepositorioMemoria(PrioridadRepositorio):
    """Implementación en memoria del repositorio de prioridades."""

    def __init__(self) -> None:
        self._prioridades: list[Prioridad] = []

    def agregar(self, prioridad: Prioridad) -> None:
        self._prioridades.append(prioridad)

    def buscar(self, documento: str, horario: str, fecha: str) -> Prioridad | None:
        doc = documento.strip()
        for p in self._prioridades:
            if p.documento == doc and p.horario == horario and p.fecha == fecha:
                return p
        return None

    def buscar_por_cupo(self, horario: str, fecha: str) -> Prioridad | None:
        for p in self._prioridades:
            if p.horario == horario and p.fecha == fecha:
                return p
        return None

    def listar(self) -> list[Prioridad]:
        return list(self._prioridades)

    def eliminar(self, prioridad: Prioridad) -> None:
        if prioridad in self._prioridades:
            self._prioridades.remove(prioridad)

    def eliminar_por_documento(self, documento: str) -> None:
        doc = documento.strip()
        self._prioridades = [p for p in self._prioridades if p.documento != doc]


