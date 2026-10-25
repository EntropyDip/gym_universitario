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

    def buscar(self, documento: str, horario: str, fecha: str,
               activa: bool | None = None) -> Reserva | None:
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









# ------------------------------------------------------------------ Repositorio de Prioridades (Angelina)
