"""Repositorios: clases abstractas y versión en memoria."""
from abc import ABC, abstractmethod
 
from modelos import Usuario
 
 
class UsuarioRepositorio(ABC):
    """Define cómo se guardan y se consultan los usuarios."""
 
    @abstractmethod
    def agregar(self, usuario: Usuario) -> None:
        """Guarda un usuario nuevo."""
 
    @abstractmethod
    def buscar(self, documento: str) -> Usuario | None:
        """Devuelve el usuario con ese documento, o None si no existe."""
 
    @abstractmethod
    def listar(self) -> list[Usuario]:
        """Devuelve una copia de la lista de usuarios."""
 
    @abstractmethod
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina el usuario con ese documento (si existe)."""
 
 
class UsuarioRepositorioMemoria(UsuarioRepositorio):
    """Guarda los usuarios en un diccionario indexado por documento."""
 
    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}
 
    def agregar(self, usuario: Usuario) -> None:
        """Guarda un usuario nuevo."""
        self._usuarios[usuario.documento] = usuario
 
    def buscar(self, documento: str) -> Usuario | None:
        """Devuelve el usuario con ese documento, o None si no existe."""
        return self._usuarios.get(documento)
 
    def listar(self) -> list[Usuario]:
        """Devuelve una copia de la lista de usuarios."""
        return list(self._usuarios.values())
 
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina el usuario con ese documento (si existe)."""
        self._usuarios.pop(documento, None)
from modelos import Reserva, Usuario

class ReservaRepositorio(ABC):
    """Define cómo se guardan y se consultan las reservas."""
 
    @abstractmethod
    def agregar(self, reserva: Reserva) -> None:
        """Guarda una reserva nueva."""
 
    @abstractmethod
    def buscar(self, documento: str, horario: str, fecha: str,
               activa: bool | None = None) -> Reserva | None:
        """Devuelve la primera reserva que coincide; activa filtra por estado si no es None."""
 
    @abstractmethod
    def listar(self) -> list[Reserva]:
        """Devuelve una copia de la lista de reservas."""
 
    @abstractmethod
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina todas las reservas de ese documento."""
 
 
class ReservaRepositorioMemoria(ReservaRepositorio):
    """Guarda las reservas en una lista en memoria."""
 
    def __init__(self) -> None:
        self._reservas: list[Reserva] = []
 
    def agregar(self, reserva: Reserva) -> None:
        """Guarda una reserva nueva."""
        self._reservas.append(reserva)
 
    def buscar(self, documento: str, horario: str, fecha: str,
               activa: bool | None = None) -> Reserva | None:
        """Devuelve la primera reserva que coincide; activa filtra por estado si no es None."""
        for reserva in self._reservas:
            if (reserva.documento == documento and reserva.horario == horario
                    and reserva.fecha == fecha
                    and (activa is None or reserva.activa == activa)):
                return reserva
        return None
 
    def listar(self) -> list[Reserva]:
        """Devuelve una copia de la lista de reservas."""
        return list(self._reservas)
 
    def eliminar_por_documento(self, documento: str) -> None:
        """Elimina todas las reservas de ese documento."""
        self._reservas = [r for r in self._reservas if r.documento != documento]
