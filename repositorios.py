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
