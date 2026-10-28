"""Repositorios: interfaces abstractas e implementaciones en memoria."""
from abc import ABC, abstractmethod
import json
import os
from pathlib import Path
import tempfile

from excepciones import CorreoInvalidoError, DatoVacioError, PersistenciaError
from modelos import ContactoUsuario, Prioridad, Reserva, Usuario, Visita

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


class ContactoUsuarioRepositorioJSON:
    """Almacena exclusivamente identificador, correo y celular en un archivo JSON.

    El archivo se vuelve a leer en cada consulta para reflejar cambios externos.
    Las escrituras reemplazan el archivo de forma atómica.
    """

    _CAMPOS = {"identificador", "correo", "celular"}

    def __init__(self, ruta: str | Path = "usuarios.json") -> None:
        """Inicializa el repositorio.

        Parámetros:
            ruta: ubicación del archivo JSON de contactos.

        Retorna:
            None.

        Excepciones:
            No accede al archivo durante la inicialización.
        """
        self.ruta = Path(ruta)

    def buscar(self, identificador: str) -> ContactoUsuario | None:
        """Busca un contacto por identificador.

        Parámetros:
            identificador: documento u otro identificador estable del usuario.

        Retorna:
            El contacto encontrado o None si no existe.

        Excepciones:
            PersistenciaError: si el archivo o sus registros no son válidos.
        """
        clave = str(identificador).strip()
        return next(
            (contacto for contacto in self.listar() if contacto.identificador == clave),
            None,
        )

    def listar(self) -> list[ContactoUsuario]:
        """Carga y valida todos los contactos guardados.

        Parámetros:
            Ninguno.

        Retorna:
            Contactos con los tres campos permitidos.

        Excepciones:
            PersistenciaError: ante errores de lectura, JSON corrupto o estructura inválida.
        """
        if not self.ruta.exists():
            return []
        try:
            with self.ruta.open("r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise PersistenciaError(
                f"No se pudieron leer los contactos desde '{self.ruta}': {error}"
            ) from error

        if not isinstance(registros, list):
            raise PersistenciaError("El archivo de contactos debe contener una lista JSON.")
        contactos: list[ContactoUsuario] = []
        for indice, registro in enumerate(registros):
            if not isinstance(registro, dict) or set(registro) != self._CAMPOS:
                raise PersistenciaError(
                    f"El registro de contacto en la posición {indice} no tiene los campos permitidos."
                )
            try:
                contactos.append(ContactoUsuario(**registro))
            except (CorreoInvalidoError, DatoVacioError, TypeError, ValueError) as error:
                raise PersistenciaError(
                    f"El registro de contacto en la posición {indice} no es válido: {error}"
                ) from error
        return contactos

    def guardar(self, contacto: ContactoUsuario) -> None:
        """Inserta o actualiza el contacto y persiste solo sus tres campos.

        Parámetros:
            contacto: datos de contacto ya validados.

        Excepciones:
            PersistenciaError: si no se puede escribir o reemplazar el archivo.

        Retorna:
            None.
        """
        contactos = {
            existente.identificador: existente
            for existente in self.listar()
        }
        contactos[contacto.identificador] = contacto
        registros = [
            {
                "identificador": item.identificador,
                "correo": item.correo,
                "celular": item.celular,
            }
            for item in contactos.values()
        ]
        self._escribir(registros)

    def eliminar(self, identificador: str) -> None:
        """Elimina el contacto del identificador indicado, si existe.

        Parámetros:
            identificador: documento u otro identificador del usuario.

        Excepciones:
            PersistenciaError: si no se puede leer o escribir el archivo.

        Retorna:
            None.
        """
        clave = str(identificador).strip()
        contactos = [item for item in self.listar() if item.identificador != clave]
        self._escribir([
            {
                "identificador": item.identificador,
                "correo": item.correo,
                "celular": item.celular,
            }
            for item in contactos
        ])

    def _escribir(self, registros: list[dict[str, str]]) -> None:
        """Reemplaza el archivo con JSON válido mediante un temporal en el mismo directorio.

        Parámetros:
            registros: lista de objetos que contienen exclusivamente los campos de contacto.

        Excepciones:
            PersistenciaError: si el directorio, temporal o reemplazo no son accesibles.

        Retorna:
            None.
        """
        temporal: str | None = None
        try:
            self.ruta.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.ruta.parent,
                prefix=f".{self.ruta.name}.",
                suffix=".tmp",
                delete=False,
            ) as archivo:
                temporal = archivo.name
                json.dump(registros, archivo, ensure_ascii=False, indent=2)
                archivo.write("\n")
            os.replace(temporal, self.ruta)
        except (OSError, TypeError, ValueError) as error:
            if temporal is not None:
                try:
                    Path(temporal).unlink()
                except FileNotFoundError:
                    pass
                except OSError:
                    pass
            raise PersistenciaError(
                f"No se pudieron guardar los contactos en '{self.ruta}': {error}"
            ) from error


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

    def listar(self) -> list[Prioridad]:
        return list(self._prioridades)

    def eliminar(self, prioridad: Prioridad) -> None:
        if prioridad in self._prioridades:
            self._prioridades.remove(prioridad)

    def eliminar_por_documento(self, documento: str) -> None:
        doc = documento.strip()
        self._prioridades = [p for p in self._prioridades if p.documento != doc]
