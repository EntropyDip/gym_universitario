"""Reglas de negocio del gimnasio (GymService)."""
from datetime import datetime, timedelta

from excepciones import (
    CupoApartadoError,
    DuracionInvalidaError,
    FechaInvalidaError,
    HorarioInvalidoError,
    PrioridadNoCumpleError,
    PrioridadNoEncontradaError,
    ReservaDuplicadaError,
    ReservaNoEncontradaError,
    UsuarioNoRegistradoError,
    UsuarioYaRegistradoError,
)
from modelos import Prioridad, Reserva, Usuario, Visita, es_fecha_valida


class GymService:
    """Orquestador de las reglas de negocio del gimnasio universitario."""

    def __init__(self, usuarios, reservas, visitas=None, prioridades=None,
                 nombre: str = "Gimnasio universitario",
                 duracion_maxima_sesion: str = "1:30 horas") -> None:
        """Inicializa el servicio inyectando los repositorios correspondientes."""
        self.nombre = nombre
        self.horarios_disponibles: list[str] = [
            "08:00 AM", "10:00 AM", "12:00 PM", "02:00 PM", "04:00 PM", "06:00 PM", "08:00 PM"
        ]
        self.duracion_maxima_sesion = duracion_maxima_sesion
        self.min_visitas_habitual: int = 3
        self.horas_limite_confirmacion: int = 2

        self.usuarios = usuarios
        self.reservas = reservas
        self.visitas = visitas
        self.prioridades = prioridades

    # =========================================================================
    # MÓDULO 1: USUARIOS Y RESERVAS (Samuel Zapata Trujillo - R1, R2, R3, R7, R8)
    # =========================================================================

    def registrar_usuario(self, nombre: str, documento: str, programa: str) -> str:
        """Registra un nuevo usuario validando que el documento sea único (R1)."""
        usuario = Usuario(nombre, documento, programa)
        if self.usuarios.buscar(usuario.documento) is not None:
            raise UsuarioYaRegistradoError(
                f"El documento {usuario.documento} ya se encuentra registrado.")
        self.usuarios.agregar(usuario)
        return f"Usuario {usuario.nombre} registrado exitosamente."

    def eliminar_usuario(self, nombre: str, documento: str) -> str:
        """Elimina un usuario y realiza la eliminación en cascada de sus datos asociados (R2)."""
        nombre_limpio = str(nombre).strip()
        doc_limpio = str(documento).strip()
        usuario = self.usuarios.buscar(doc_limpio)
        if usuario is None or usuario.nombre != nombre_limpio:
            raise UsuarioNoRegistradoError("El usuario no está registrado.")

        # Eliminación en cascada en todos los repositorios asociados
        for repositorio in (self.reservas, self.visitas, self.prioridades):
            if repositorio is not None:
                repositorio.eliminar_por_documento(doc_limpio)

        self.usuarios.eliminar_por_documento(doc_limpio)
        return f"El usuario identificado con {doc_limpio} se eliminó correctamente."

    def listar_usuarios(self) -> list[Usuario]:
        """Devuelve la lista de usuarios registrados."""
        return self.usuarios.listar()

    def realizar_reserva(self, documento: str, horario_deseado: str, fecha: str,
                         hora_actual: datetime | None = None) -> str:
        """Crea una reserva activa aplicando todas las validaciones de negocio (R3)."""
        doc_limpio = str(documento).strip()
        usuario = self._exigir_usuario(doc_limpio)
        self._validar_fecha(fecha)

        ahora = hora_actual or datetime.now()
        self._liberar_prioridades_vencidas(ahora)
        self._validar_horario(horario_deseado)

        # Validar si el cupo está apartado con prioridad
        prioridad = self._prioridad_del_cupo(horario_deseado, fecha)
        if prioridad is not None:
            if prioridad.documento != doc_limpio:
                raise CupoApartadoError(
                    f"El horario {horario_deseado} del {fecha} está apartado "
                    f"con prioridad para {prioridad.nombre}.")
            raise ReservaDuplicadaError(
                f"{usuario.nombre} ya tiene este horario apartado con prioridad. "
                f"No es necesario hacer otra reserva.")

        # Validar que no tenga otra reserva activa en la misma fecha
        self._exigir_sin_reserva_activa(doc_limpio, usuario.nombre, fecha)

        nueva_reserva = Reserva(doc_limpio, usuario.nombre, horario_deseado, fecha)
        self.reservas.agregar(nueva_reserva)
        return (f"¡Reserva exitosa! {usuario.nombre} tiene su espacio a las "
                f"{horario_deseado}. El tiempo para estar haciendo uso del gym es: "
                f"{self.duracion_maxima_sesion}.")

    def cancelar_reserva(self, documento: str, horario: str, fecha: str) -> str:
        """Cancela una reserva activa; si ya está cancelada lo notifica sin error (R7)."""
        doc_limpio = str(documento).strip()
        reserva = (self.reservas.buscar(doc_limpio, horario, fecha, activa=True)
                   or self.reservas.buscar(doc_limpio, horario, fecha))
        if reserva is None:
            raise ReservaNoEncontradaError("No existe una reserva con esos datos.")
        return reserva.cancelar()

    def confirmar_reserva(self, documento: str, horario: str, fecha: str,
                          hora_actual: datetime | None = None) -> str:
        """Reactiva una reserva previamente cancelada (R8)."""
        doc_limpio = str(documento).strip()
        reserva = (self.reservas.buscar(doc_limpio, horario, fecha, activa=False)
                   or self.reservas.buscar(doc_limpio, horario, fecha))
        if reserva is None:
            raise ReservaNoEncontradaError("No se encontró una reserva con esos datos.")
        if reserva.activa:
            return reserva.confirmar()

        ahora = hora_actual or datetime.now()
        self._liberar_prioridades_vencidas(ahora)

        prioridad = self._prioridad_del_cupo(horario, fecha)
        if prioridad is not None and prioridad.documento != doc_limpio:
            raise CupoApartadoError(
                f"El horario {horario} del {fecha} está apartado "
                f"con prioridad para {prioridad.nombre}.")

        self._exigir_sin_reserva_activa(doc_limpio, reserva.nombre_usuario, fecha)
        return reserva.confirmar()

    def listar_reservas(self) -> list[Reserva]:
        """Devuelve la lista de reservas registradas."""
        return self.reservas.listar()
 
    # =========================================================================
    # MÓDULO 2: VISITAS Y ESTADÍSTICAS (Juan José Aguirre - R4, R5, R6, R11, R15)
    # =========================================================================













    # =========================================================================
    # MÓDULO 3: PRIORIDADES Y CONSULTAS (Angelina Negrette - R9, R10, R12, R13, R14)
    # =========================================================================
    def verificar_propietario_reserva(self, documento: str) -> str:
        """Indica si el usuario tiene al menos una reserva activa o histórica (R9)."""
        doc_limpio = str(documento).strip()
        for r in self.listar_reservas():
            if r.coincide_con(doc_limpio):
                return "Sí"
        return "No"

    def mostrar_resumen_reserva(self, documento: str) -> str:
        """Muestra el resumen de la reserva más relevante del usuario (R10)."""
        doc_limpio = str(documento).strip()
        reservas = [r for r in self.listar_reservas() if r.coincide_con(doc_limpio)]
        if not reservas:
            raise ReservaNoEncontradaError(f"No hay reservas asociadas al documento {doc_limpio}.")

        # Priorizar la reserva activa más reciente
        activas = [r for r in reservas if r.activa]
        seleccionada = activas[-1] if activas else reservas[-1]
        return seleccionada.mostrar_resumen()

    def consultar_disponibilidad(self, fecha: str,
                                 hora_actual: datetime | None = None) -> list[tuple[str, str, str]]:
        """Retorna la disponibilidad detallada (libre, reservado, apartado) por horario (R14)."""
        self._validar_fecha(fecha)
        ahora = hora_actual or datetime.now()
        self._liberar_prioridades_vencidas(ahora)

        resultados = []
        for horario in self.horarios_disponibles:
            prioridad = self._prioridad_del_cupo(horario, fecha)
            if prioridad is not None:
                estado_p = "confirmada" if prioridad.confirmada else "pendiente"
                resultados.append((
                    horario,
                    "apartado",
                    f"Apartado ({estado_p}) por {prioridad.nombre} ({prioridad.documento})"
                ))
                continue

            reserva_activa = None
            for r in self.listar_reservas():
                if r.horario == horario and r.fecha == fecha and r.activa:
                    reserva_activa = r
                    break

            if reserva_activa is not None:
                resultados.append((
                    horario,
                    "reservado",
                    f"Reservado por {reserva_activa.nombre_usuario} ({reserva_activa.documento})"
                ))
            else:
                resultados.append((horario, "libre", "Cupo disponible"))

        return resultados






