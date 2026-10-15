from datetime import datetime

from excepciones import (CupoApartadoError, FechaInvalidaError, HorarioInvalidoError,
                         ReservaDuplicadaError, ReservaNoEncontradaError,
                         UsuarioNoRegistradoError, UsuarioYaRegistradoError)
from modelos import Reserva, Usuario, es_fecha_valida

    # ---------------------------------------------------------------- R3, R7, R8
    def realizar_reserva(self, documento: str, horario_deseado: str, fecha: str,
                         hora_actual: datetime | None = None) -> str:
        """Crea una reserva activa (R3).

        Orden de validaciones: usuario, fecha, liberar prioridades vencidas,
        horario, prioridad de otro, reserva activa.
        """
        documento = documento.strip()
        usuario = self._exigir_usuario(documento)
        self._validar_fecha(fecha)
        self._liberar_prioridades_vencidas(hora_actual or datetime.now())
        self._validar_horario(horario_deseado)

        prioridad = self._prioridad_del_cupo(horario_deseado, fecha)
        if prioridad is not None:
            if prioridad.documento != documento:
                raise CupoApartadoError(
                    f"El horario {horario_deseado} del {fecha} está apartado "
                    f"con prioridad para {prioridad.nombre}.")
            raise ReservaDuplicadaError(
                f"{usuario.nombre} ya tiene este horario apartado con prioridad. "
                f"No es necesario hacer otra reserva.")

        self._exigir_sin_reserva_activa(documento, usuario.nombre, fecha)

        self.reservas.agregar(Reserva(documento, usuario.nombre, horario_deseado, fecha))
        return (f"¡Reserva exitosa! {usuario.nombre} tiene su espacio a las "
                f"{horario_deseado}. El tiempo para estar haciendo uso del gym es: "
                f"{self.duracion_maxima_sesion}.")

    def cancelar_reserva(self, documento: str, horario: str, fecha: str) -> str:
        """Cancela una reserva (R7); si hay una activa y otra cancelada, actúa sobre la activa."""
        documento = documento.strip()
        reserva = (self.reservas.buscar(documento, horario, fecha, activa=True)
                   or self.reservas.buscar(documento, horario, fecha))
        if reserva is None:
            raise ReservaNoEncontradaError("No existe una reserva con esos datos.")
        return reserva.cancelar()

    def confirmar_reserva(self, documento: str, horario: str, fecha: str,
                          hora_actual: datetime | None = None) -> str:
        """Reactiva una reserva cancelada (R8) respetando RN3 y RN7."""
        documento = documento.strip()
        reserva = (self.reservas.buscar(documento, horario, fecha, activa=False)
                   or self.reservas.buscar(documento, horario, fecha))
        if reserva is None:
            raise ReservaNoEncontradaError("No se encontró una reserva con esos datos.")
        if reserva.activa:
            return reserva.confirmar()  # solo informa que ya estaba activa

        self._liberar_prioridades_vencidas(hora_actual or datetime.now())
        prioridad = self._prioridad_del_cupo(horario, fecha)
        if prioridad is not None and prioridad.documento != documento:
            raise CupoApartadoError(
                f"El horario {horario} del {fecha} está apartado "
                f"con prioridad para {prioridad.nombre}.")
        self._exigir_sin_reserva_activa(documento, reserva.nombre_usuario, fecha)
        return reserva.confirmar()

    def listar_reservas(self) -> list[Reserva]:
        """Devuelve las reservas registradas (para las tablas de la interfaz)."""
        return self.reservas.listar()


# ------------------------------------------------------------------ apoyo
    def _exigir_usuario(self, documento: str) -> Usuario:
        """Devuelve el usuario o lanza UsuarioNoRegistradoError."""
        usuario = self.usuarios.buscar(documento)
        if usuario is None:
            raise UsuarioNoRegistradoError(
                f"El documento {documento} no está registrado para hacer la reserva.")
        return usuario

    def _validar_fecha(self, fecha: str) -> None:
        """Lanza FechaInvalidaError si la fecha no es AAAA-MM-DD válida."""
        if not es_fecha_valida(fecha):
            raise FechaInvalidaError(
                "La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15.")

    def _validar_horario(self, horario: str) -> None:
        """Lanza HorarioInvalidoError (con la lista de horarios) si el horario no existe."""
        if horario not in self.horarios_disponibles:
            raise HorarioInvalidoError(
                f"El horario '{horario}' no existe.\n"
                f"Horarios disponibles: {' | '.join(self.horarios_disponibles)}\n"
                f"Tiempo máximo permitido por sesión: {self.duracion_maxima_sesion}.")

    def _prioridad_del_cupo(self, horario: str, fecha: str):
        """Devuelve la prioridad que aparta ese horario y fecha, o None."""
        if self.prioridades is None:
            return None
        for prioridad in self.prioridades.listar():
            if prioridad.horario == horario and prioridad.fecha == fecha:
                return prioridad
        return None

    def _exigir_sin_reserva_activa(self, documento: str, nombre: str, fecha: str) -> None:
        """Lanza ReservaDuplicadaError si el usuario ya tiene una reserva activa ese día."""
        for reserva in self.reservas.listar():
            if reserva.documento == documento and reserva.fecha == fecha and reserva.activa:
                raise ReservaDuplicadaError(
                    f"El usuario {nombre} ya tiene una reserva activa el {fecha}.")

    def _liberar_prioridades_vencidas(self, hora_actual: datetime) -> None:
        """Elimina las prioridades no confirmadas cuyo límite ya pasó.

        Provisional: Angelina lo implementa en HU-08 (necesita Prioridad.esta_vencida).
        """
        if self.prioridades is None:
            return

