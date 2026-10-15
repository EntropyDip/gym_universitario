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
                  
    def registrar_usuario(self, nombre: str, documento: str, programa: str) -> str:
        """Registra un usuario nuevo (R1). Lanza DatoVacioError o UsuarioYaRegistradoError."""
        usuario = Usuario(nombre, documento, programa)  # valida y quita espacios
        if self.usuarios.buscar(usuario.documento) is not None:
            raise UsuarioYaRegistradoError(
                f"El documento {usuario.documento} ya se encuentra registrado.")
        self.usuarios.agregar(usuario)
        return f"Usuario {usuario.nombre} registrado exitosamente."

    def eliminar_usuario(self, nombre: str, documento: str) -> str:
        """Elimina un usuario con sus reservas, visitas y prioridades (R2)."""
        nombre, documento = nombre.strip(), documento.strip()
        usuario = self.usuarios.buscar(documento)
        if usuario is None or usuario.nombre != nombre:
            raise UsuarioNoRegistradoError("El usuario no está registrado.")
        for repositorio in (self.reservas, self.visitas, self.prioridades):
            if repositorio is not None:
                repositorio.eliminar_por_documento(documento)
        self.usuarios.eliminar_por_documento(documento)
        return f"El usuario identificado con {documento} se eliminó correctamente."

    def listar_usuarios(self) -> list[Usuario]:
        """Devuelve los usuarios registrados (para las tablas de la interfaz)."""
        return self.usuarios.listar()
