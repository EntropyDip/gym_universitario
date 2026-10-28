"""Reglas de negocio del gimnasio (GymService)."""
from datetime import datetime, timedelta

from excepciones import (
    CorreoInvalidoError,
    CupoLlenoError,
    DatosContactoRequeridosError,
    FechaInvalidaError,
    HorarioInvalidoError,
    PrioridadNoCumpleError,
    PrioridadNoEncontradaError,
    ReservaDuplicadaError,
    ReservaNoEncontradaError,
    UsuarioNoRegistradoError,
    UsuarioYaRegistradoError,
    VisitaDuplicadaError,
)
from modelos import ContactoUsuario, Prioridad, Reserva, Usuario, Visita, es_fecha_valida
from notificador import NotificadorReservas


class GymService:
    """Orquestador de las reglas de negocio del gimnasio universitario."""

    def __init__(self, usuarios, reservas, visitas=None, prioridades=None,
                nombre: str = "Gimnasio universitario",
                duracion_maxima_sesion: str = "1:30 horas",
                capacidad_maxima: int = 15, contactos=None,
                notificador: NotificadorReservas | None = None) -> None:
        """Inicializa el servicio y sus dependencias de persistencia y notificación.

        Parámetros:
            usuarios: repositorio de usuarios de dominio.
            reservas: repositorio de reservas.
            visitas: repositorio opcional de visitas.
            prioridades: repositorio opcional de prioridades.
            nombre: nombre mostrado para el gimnasio.
            duracion_maxima_sesion: duración máxima mostrada en confirmaciones.
            capacidad_maxima: aforo máximo por franja horaria.
            contactos: repositorio opcional de contactos, habitualmente JSON.
            notificador: notificador opcional; se crea uno predeterminado si se omite.

        Retorna:
            None.

        Excepciones:
            No valida ni accede a los repositorios durante la construcción.
        """
        self.nombre = nombre
        self.horarios_disponibles: list[str] = [
            "08:00 AM", "10:00 AM", "12:00 PM", "02:00 PM", "04:00 PM", "06:00 PM", "08:00 PM"
        ]
        self.duracion_maxima_sesion = duracion_maxima_sesion
        self.min_visitas_habitual: int = 3
        self.horas_limite_confirmacion: int = 2
        self.capacidad_maxima: int = capacidad_maxima
        self.max_reservas_semana: int = 3            
        self.usuarios = usuarios
        self.reservas = reservas
        self.visitas = visitas
        self.prioridades = prioridades
        self.contactos = contactos
        self.notificador = notificador or NotificadorReservas()

    def registrar_usuario(self, nombre: str, documento: str, programa: str,
                          correo: str = "", celular: str = "") -> str:
        """Registra un nuevo usuario validando que el documento sea único (R1).

        Parámetros:
            nombre: nombre del usuario.
            documento: identificador único.
            programa: programa académico.
            correo: correo opcional para la notificación de reserva.
            celular: número de celular opcional para el respaldo SMS/WhatsApp.

        Retorna:
            Mensaje de éxito.

        Excepciones:
            UsuarioYaRegistradoError: si el documento ya está registrado.
            CorreoInvalidoError: si se proporciona un correo inválido.
            DatoVacioError: si faltan datos obligatorios del usuario o contacto.
            PersistenciaError: si no se puede persistir el contacto.
        """
        usuario = Usuario(nombre, documento, programa, correo)
        if self.usuarios.buscar(usuario.documento) is not None:
            raise UsuarioYaRegistradoError(
                f"El documento {usuario.documento} ya se encuentra registrado.")
        if self.contactos is not None and (correo.strip() or celular.strip()):
            contacto = ContactoUsuario(usuario.documento, correo, celular)
            self.contactos.guardar(contacto)
        self.usuarios.agregar(usuario)
        return f"Usuario {usuario.nombre} registrado exitosamente."

    def eliminar_usuario(self, nombre: str, documento: str) -> str:
        """Elimina el usuario y sus reservas, visitas, prioridades y contacto (R2).

        Parámetros:
            nombre: nombre que debe coincidir con el registro.
            documento: identificador único del usuario.

        Retorna:
            Mensaje de éxito.

        Excepciones:
            UsuarioNoRegistradoError: si el nombre/documento no coincide.
            PersistenciaError: si no se puede eliminar el contacto JSON.
        """
        nombre_limpio = str(nombre).strip()
        doc_limpio = str(documento).strip()
        usuario = self.usuarios.buscar(doc_limpio)
        if usuario is None or usuario.nombre != nombre_limpio:
            raise UsuarioNoRegistradoError("El usuario no está registrado.")

        if self.contactos is not None:
            self.contactos.eliminar(doc_limpio)

        # Eliminación en cascada en todos los repositorios asociados
        for repositorio in (self.reservas, self.visitas, self.prioridades):
            if repositorio is not None:
                repositorio.eliminar_por_documento(doc_limpio)

        self.usuarios.eliminar_por_documento(doc_limpio)
        return f"El usuario identificado con {doc_limpio} se eliminó correctamente."

    def obtener_contacto_usuario(self, identificador: str) -> ContactoUsuario | None:
        """Busca en persistencia el contacto asociado al identificador.

        Parámetros:
            identificador: documento u otro identificador estable del usuario.

        Retorna:
            El correo y celular guardados, o None cuando aún no hay registro.

        Excepciones:
            PersistenciaError: si el archivo JSON no se puede leer o validar.
        """
        if self.contactos is None:
            return None
        return self.contactos.buscar(str(identificador).strip())

    def listar_usuarios(self) -> list[Usuario]:
        """Devuelve la lista de usuarios registrados."""
        return self.usuarios.listar()

    def realizar_reserva(self, documento: str, horario_deseado: str, fecha: str,
                         hora_actual: datetime | None = None,
                         correo: str | None = None,
                         celular: str | None = None) -> str:
        """Crea una reserva y notifica al usuario por correo o por el canal alternativo.

        Si existe persistencia de contactos, la consulta se hace antes de reservar.
        Cuando no existe el contacto, el llamador debe proporcionar correo y celular;
        solo se guardan tras validar todas las reglas de reserva.

        Parámetros:
            documento: identificador del usuario ya registrado.
            horario_deseado: franja solicitada.
            fecha: fecha de la reserva en formato AAAA-MM-DD.
            hora_actual: hora opcional para reglas temporales.
            correo: correo requerido para registrar un contacto nuevo.
            celular: celular requerido para registrar un contacto nuevo.

        Retorna:
            Mensaje con la confirmación de la reserva.

        Excepciones:
            UsuarioNoRegistradoError, FechaInvalidaError, HorarioInvalidoError,
            ReservaDuplicadaError, CupoLlenoError, DatosContactoRequeridosError,
            CorreoInvalidoError, DatoVacioError o PersistenciaError según corresponda.
        """
        doc_limpio = str(documento).strip()
        horario_deseado = str(horario_deseado).strip()
        fecha = str(fecha).strip()
        usuario = self._exigir_usuario(doc_limpio)
        contacto_guardado = self.obtener_contacto_usuario(doc_limpio)
        self._validar_fecha(fecha)
        ahora = hora_actual or datetime.now()
        self._liberar_prioridades_vencidas(ahora)
        self._validar_horario(horario_deseado)


        # Quien ya tiene prioridad en la franja tiene su cupo garantizado
        if self._prioridad_del_usuario(doc_limpio, horario_deseado, fecha) is not None:
            raise ReservaDuplicadaError(
                f"{usuario.nombre} ya tiene este horario apartado con prioridad. "
                f"No es necesario hacer otra reserva.")


        # Validar que no tenga otra reserva activa en la misma fecha
        self._exigir_sin_reserva_activa(doc_limpio, usuario.nombre, fecha)
        # Valiidar que no supere el límite de reservas activas por semana
        self._exigir_limite_semanal(doc_limpio, usuario.nombre, fecha)
        # Validar que la franja no haya alcanzado el máximo de usuarios
        self._exigir_cupo(doc_limpio, horario_deseado, fecha)

        contacto = contacto_guardado
        if self.contactos is not None and contacto is None:
            if not correo or not celular:
                raise DatosContactoRequeridosError(
                    "Para reservar por primera vez, ingresa correo electrónico y número de celular."
                )
            contacto = ContactoUsuario(doc_limpio, correo, celular)
            self.contactos.guardar(contacto)

        nueva_reserva = Reserva(doc_limpio, usuario.nombre, horario_deseado, fecha)
        self.reservas.agregar(nueva_reserva)
        mensaje = (f"¡Reserva exitosa! {usuario.nombre} tiene su espacio a las "
                   f"{horario_deseado}. El tiempo para estar haciendo uso del gym es: "
                   f"{self.duracion_maxima_sesion}.")
        correo_destino = contacto.correo if contacto else usuario.correo
        celular_destino = contacto.celular if contacto else ""
        if correo_destino or celular_destino:
            self.notificador.notificar_reserva(
                destinatario=correo_destino,
                celular=celular_destino,
                nombre_usuario=usuario.nombre,
                horario=horario_deseado,
                fecha=fecha,
            )
        return mensaje

    def cancelar_reserva(self, documento: str, horario: str, fecha: str) -> str:
        """Cancela una reserva activa; si ya está cancelada lo notifica sin error (R7)."""
        doc_limpio = str(documento).strip()
        horario = str(horario).strip()
        fecha = str(fecha).strip()
        reserva = (self.reservas.buscar(doc_limpio, horario, fecha, activa=True) or self.reservas.buscar(doc_limpio, horario, fecha))
        if reserva is None:
            raise ReservaNoEncontradaError("No existe una reserva con esos datos.")
        return reserva.cancelar()

    def confirmar_reserva(self, documento: str, horario: str, fecha: str, hora_actual: datetime | None = None) -> str:
        """Reactiva una reserva cancelada y notifica usando el contacto persistido.

        Parámetros:
            documento: identificador del titular.
            horario: franja original de la reserva.
            fecha: fecha original de la reserva.
            hora_actual: hora opcional para las validaciones temporales.

        Retorna:
            Mensaje con el resultado de la reactivación.

        Excepciones:
            ReservaNoEncontradaError, ReservaDuplicadaError, CupoLlenoError,
            PersistenciaError si no puede consultarse el contacto almacenado.
        """
        doc_limpio = str(documento).strip()
        horario = str(horario).strip()
        fecha = str(fecha).strip()
        reserva = (self.reservas.buscar(doc_limpio, horario, fecha, activa=False) or self.reservas.buscar(doc_limpio, horario, fecha))
        if reserva is None:
            raise ReservaNoEncontradaError("No se encontró una reserva con esos datos.")
        if reserva.activa:
            return reserva.confirmar()

        ahora = hora_actual or datetime.now()
        self._liberar_prioridades_vencidas(ahora)

        if self._prioridad_del_usuario(doc_limpio, horario, fecha) is not None:
            raise ReservaDuplicadaError(
                f"{reserva.nombre_usuario} ya tiene este horario apartado con prioridad.")
        self._exigir_sin_reserva_activa(doc_limpio, reserva.nombre_usuario, fecha)
        self._exigir_limite_semanal(doc_limpio, reserva.nombre_usuario, fecha)
        self._exigir_cupo(doc_limpio, horario, fecha)
        usuario = self.usuarios.buscar(doc_limpio)
        contacto = self.obtener_contacto_usuario(doc_limpio)
        resultado = reserva.confirmar()
        correo_destino = contacto.correo if contacto else (usuario.correo if usuario else "")
        celular_destino = contacto.celular if contacto else ""
        if correo_destino or celular_destino:
            self.notificador.notificar_reserva(
                destinatario=correo_destino,
                celular=celular_destino,
                nombre_usuario=reserva.nombre_usuario,
                horario=horario,
                fecha=fecha,
            )
        return resultado


    def listar_reservas(self) -> list[Reserva]:
        """Devuelve la lista de reservas registradas."""
        return self.reservas.listar()

    def registrar_visita(self, documento: str, horario: str, duracion: int, equipos: list[str], fecha: str | None = None, hora_actual: datetime | None = None) -> str:
        """Registra la asistencia de un usuario con los equipos usados (R4)."""
        doc_limpio = str(documento).strip()
        horario = str(horario).strip()
        ahora = hora_actual or datetime.now()
        fecha_visita = str(fecha).strip() if fecha else ahora.strftime("%Y-%m-%d")
        usuario = self._exigir_usuario(doc_limpio)
        self._validar_horario(horario)
        self._validar_fecha(fecha_visita)

        nueva_visita = Visita(doc_limpio, horario, duracion, equipos, fecha_visita)

        # Un usuario no puede tener dos visitas en la misma fecha y horario
        for v in self.listar_visitas():
            if v.documento == doc_limpio and v.horario == horario and v.fecha == fecha_visita:
                raise VisitaDuplicadaError(
                    f"{usuario.nombre} ya tiene una visita registrada el "
                    f"{fecha_visita} a las {horario}.")

        self._liberar_prioridades_vencidas(ahora)
        self._exigir_cupo(doc_limpio, horario, fecha_visita)
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

    def datos_promedio_duracion(self) -> list[tuple[str, float]]:
        """Calcula los promedios numéricos de duración para alimentar gráficos y tablas."""
        visitas = self.listar_visitas()
        if not visitas:
            return []

        suma: dict[str, int] = {}
        conteo: dict[str, int] = {}
        for v in visitas:
            suma[v.documento] = suma.get(v.documento, 0) + v.duracion
            conteo[v.documento] = conteo.get(v.documento, 0) + 1

        resultados = []
        for doc, total in suma.items():
            promedio = round(total / conteo[doc], 1)
            usuario = self.usuarios.buscar(doc)
            nombre = f"{usuario.nombre} ({doc})" if usuario else doc
            resultados.append((nombre, promedio))
        return sorted(resultados, key=lambda x: x[1], reverse=True)

    def equipo_mas_utilizado(self) -> str:
        """Determina el equipo deportivo con mayor frecuencia de uso (R15)."""
        ranking = self.ranking_equipos()
        if not ranking:
            return "No hay registros de uso de equipos."
        top_equipo, usos = ranking[0]
        return f"El equipo más utilizado es {top_equipo} con {usos} usos registrados."

    def ranking_equipos(self) -> list[tuple[str, int]]:
        """Calcula el ranking de equipos ordenado de mayor a menor frecuencia de uso."""
        visitas = self.listar_visitas()
        if not visitas:
            return []

        conteo: dict[str, int] = {}
        for v in visitas:
            # Cuenta una vez por visita cada equipo sin distinguir mayúsculas
            vistos_en_visita = {eq.title() for eq in v.equipos if eq.strip()}
            for eq in vistos_en_visita:
                conteo[eq] = conteo.get(eq, 0) + 1

        return sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    
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

    def consultar_disponibilidad(self, fecha: str, hora_actual: datetime | None = None) -> list[tuple[str, str, str]]:
        """Retorna la disponibilidad detallada (libre, reservado, apartado) por horario (R14)."""
        fecha = str(fecha).strip()
        self._validar_fecha(fecha)
        self._liberar_prioridades_vencidas(hora_actual or datetime.now())

        resultados = []
        for horario in self.horarios_disponibles:
            ocupados = len(self._ocupantes(horario, fecha))
            libres = max(self.capacidad_maxima - ocupados, 0)
            if ocupados == 0:
                estado = "libre"
            elif libres == 0:
                estado = "lleno"
            else:
                estado = "parcial"
            resultados.append((
                horario,
                estado,
                f"{ocupados}/{self.capacidad_maxima} usuarios · {libres} cupos libres"
            ))
        return resultados
        
    def ocupantes_franja(self, fecha: str, horario: str,
                         hora_actual: datetime | None = None) -> list[tuple[str, str, str]]:
        """Lista (nombre, documento, participación) de quienes reservaron, visitaron o tienen prioridad (R14)."""
        fecha = str(fecha).strip()
        horario = str(horario).strip()
        self._validar_fecha(fecha)
        self._validar_horario(horario)
        self._liberar_prioridades_vencidas(hora_actual or datetime.now())
        return self._ocupantes(horario, fecha)


    def prioridad_membresia(self, documento: str, horario: str, fecha: str,
                            hora_actual: datetime | None = None) -> str:
        """Otorga exclusividad sobre un cupo si es habitual (>=3) o acumula más tiempo (R12)."""
        doc_limpio = str(documento).strip()
        horario_limpio = str(horario).strip() 
        fecha_limpia = str(fecha).strip()    
        
        usuario = self._exigir_usuario(doc_limpio)
        self._validar_horario(horario_limpio) 
        self._validar_fecha(fecha_limpia)     

        ahora = hora_actual or datetime.now()
        self._liberar_prioridades_vencidas(ahora)

        # Validar si faltan menos de 2 horas para el horario
        hora_del_horario = datetime.strptime(f"{fecha_limpia} {horario_limpio}", "%Y-%m-%d %I:%M %p")
        limite_minimo = hora_del_horario - timedelta(hours=self.horas_limite_confirmacion)
        if ahora > limite_minimo:
            raise PrioridadNoCumpleError(
                f"No se puede solicitar prioridad con menos de "
                f"{self.horas_limite_confirmacion} horas de antelación.")

        # Verificar si ya tiene prioridad o una reserva activa en la franja
        if self._prioridad_del_usuario(doc_limpio, horario_limpio, fecha_limpia) is not None:
            return (f"{usuario.nombre} ya tiene prioridad para el horario "
                    f"{horario_limpio} del {fecha_limpia}.")
        if self.reservas.buscar(doc_limpio, horario_limpio, fecha_limpia, activa=True) is not None:
            raise ReservaDuplicadaError(
                f"{usuario.nombre} ya tiene una reserva activa en ese horario; "
                f"no necesita prioridad.")

        # Criterio 1: Usuario habitual en ese horario específico (>= 3 visitas registradas)
        visitas_usuario = [v for v in self.listar_visitas() if v.documento == doc_limpio]
        veces_en_horario = sum(1 for v in visitas_usuario if v.horario == horario_limpio)
        es_habitual = veces_en_horario >= self.min_visitas_habitual

        # Criterio 2: Mayor tiempo total acumulado (estricto, sin empates)
        tiempo_por_usuario: dict[str, int] = {}
        for v in self.listar_visitas():
            tiempo_por_usuario[v.documento] = tiempo_por_usuario.get(v.documento, 0) + v.duracion

        tiempo_usuario = tiempo_por_usuario.get(doc_limpio, 0)
        tiene_mas_tiempo = tiempo_usuario > 0
        for otro_doc, otro_tiempo in tiempo_por_usuario.items():
            if otro_doc != doc_limpio and otro_tiempo >= tiempo_usuario:
                tiene_mas_tiempo = False
                break

        if not es_habitual and not tiene_mas_tiempo:
            raise PrioridadNoCumpleError(
                f"{usuario.nombre} no cumple los requisitos para tener prioridad "
                f"en el horario {horario_limpio} (requiere >={self.min_visitas_habitual} "
                f"visitas en ese horario o mayor tiempo total acumulado).")

        self._exigir_cupo(doc_limpio, horario_limpio, fecha_limpia)
        nueva_prioridad = Prioridad(doc_limpio, usuario.nombre, horario_limpio, fecha_limpia, ahora)
        if self.prioridades is not None:
            self.prioridades.agregar(nueva_prioridad)

        return (f"{usuario.nombre} obtuvo prioridad para el horario {horario_limpio} del {fecha_limpia}. "
                f"Tiene hasta 2 horas antes del horario para confirmar su asistencia.")

    def confirmar_prioridad(self, documento: str, horario: str, fecha: str,
                            hora_actual: datetime | None = None) -> str:
        """Confirma la asistencia o libera el cupo si venció el límite de 2 horas (R13)."""
        doc_limpio = str(documento).strip()
        if self.prioridades is None:
            raise PrioridadNoEncontradaError("No existen prioridades registradas.")

        prioridad = self.prioridades.buscar(doc_limpio, horario, fecha)
        if prioridad is None:
            raise PrioridadNoEncontradaError("No se encontró una prioridad con esos datos.")

        if prioridad.confirmada:
            return f"{prioridad.nombre} ya había confirmado el cupo de las {horario} del {fecha}."

        ahora = hora_actual or datetime.now()
        if prioridad.esta_vencida(ahora):
            self.prioridades.eliminar(prioridad)
            return (f"{prioridad.nombre} no confirmó a tiempo. "
                    f"El cupo de las {horario} del {fecha} queda libre.")

        prioridad.confirmar()
        return (f"{prioridad.nombre} confirmó su asistencia. "
                f"El cupo de las {horario} del {fecha} queda garantizado.")

    def listar_prioridades(self) -> list[Prioridad]:
        """Devuelve la lista de prioridades registradas."""
        if self.prioridades is None:
            return []
        return self.prioridades.listar()

    def listar_prioridades_vigentes(self, hora_actual: datetime | None = None) -> list[Prioridad]:
        """Libera las prioridades vencidas y devuelve solo las vigentes (para la interfaz)."""
        self._liberar_prioridades_vencidas(hora_actual or datetime.now())
        return self.listar_prioridades()

    def _exigir_usuario(self, documento: str) -> Usuario:
        """Valida que el usuario exista en el repositorio o lanza excepción."""
        usuario = self.usuarios.buscar(documento)
        if usuario is None:
            raise UsuarioNoRegistradoError(
                f"El documento {documento} no está registrado.")
        return usuario

    def _validar_fecha(self, fecha: str) -> None:
        """Valida matemáticamente el formato y existencia de la fecha."""
        if not es_fecha_valida(fecha):
            raise FechaInvalidaError(
                "La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15.")

    def _validar_horario(self, horario: str) -> None:
        """Valida que el horario solicitado pertenezca a la agenda del gimnasio."""
        if horario not in self.horarios_disponibles:
            agenda = " | ".join(self.horarios_disponibles)
            raise HorarioInvalidoError(
                f"El horario '{horario}' no existe.\n"
                f"Horarios disponibles: {agenda}\n"
                f"Tiempo máximo permitido por sesión: {self.duracion_maxima_sesion}.")

    def _prioridad_del_usuario(self, documento: str, horario: str, fecha: str) -> Prioridad | None:
        """Devuelve la prioridad vigente del usuario en una franja, si existe."""
        if self.prioridades is None:
            return None
        return self.prioridades.buscar(documento, horario, fecha)

    def _ocupantes(self, horario: str, fecha: str) -> list[tuple[str, str, str]]:
        """Reúne sin repetir a quienes reservaron, visitaron o tienen prioridad en la franja."""
        ocupantes: dict[str, tuple[str, list[str]]] = {}

        def sumar(documento: str, nombre: str, participacion: str) -> None:
            _, tipos = ocupantes.setdefault(documento, (nombre, []))
            if participacion not in tipos:
                tipos.append(participacion)

        for r in self.listar_reservas():
            if r.horario == horario and r.fecha == fecha and r.activa:
                sumar(r.documento, r.nombre_usuario, "Reserva")
        for v in self.listar_visitas():
            if v.horario == horario and v.fecha == fecha:
                usuario = self.usuarios.buscar(v.documento)
                sumar(v.documento, usuario.nombre if usuario else v.documento, "Visita")
        for p in self.listar_prioridades():
            if p.horario == horario and p.fecha == fecha:
                sumar(p.documento, p.nombre, "Prioridad")

        return [(nombre, doc, ", ".join(tipos)) for doc, (nombre, tipos) in ocupantes.items()]

    def _exigir_cupo(self, documento: str, horario: str, fecha: str) -> None:
        """Verifica que la franja no esté llena; quien ya cuenta en ella no ocupa un cupo nuevo."""
        ocupantes = self._ocupantes(horario, fecha)
        if any(doc == documento for _, doc, _ in ocupantes):
            return
        if len(ocupantes) >= self.capacidad_maxima:
            raise CupoLlenoError(
                f"El horario {horario} del {fecha} ya alcanzó el máximo de "
                f"{self.capacidad_maxima} usuarios.")

    def _exigir_sin_reserva_activa(self, documento: str, nombre: str, fecha: str) -> None:
        """Verifica que un usuario no tenga más de una reserva activa en la misma fecha."""
        for reserva in self.listar_reservas():
            if reserva.documento == documento and reserva.fecha == fecha and reserva.activa:
                raise ReservaDuplicadaError(
                    f"El usuario {nombre} ya tiene una reserva activa el {fecha}.")
                
    def _exigir_limite_semanal(self, documento: str, nombre: str, fecha: str) -> None:
        """Verifica que el usuario no supere las reservas activas permitidas por semana."""
        semana = datetime.strptime(fecha, "%Y-%m-%d").isocalendar()[:2]
        activas = [
            r for r in self.listar_reservas()
            if r.documento == documento and r.activa
            and datetime.strptime(r.fecha, "%Y-%m-%d").isocalendar()[:2] == semana
        ]
        if len(activas) >= self.max_reservas_semana:
            raise ReservaDuplicadaError(
                f"{nombre} ya alcanzó el máximo de {self.max_reservas_semana} reservas "
                f"activas en la semana de {fecha}.")

    def _liberar_prioridades_vencidas(self, hora_actual: datetime) -> None:
        """Elimina del sistema las prioridades sin confirmar que hayan superado el límite."""
        if self.prioridades is None:
            return
        vencidas = [p for p in self.prioridades.listar() if p.esta_vencida(hora_actual)]
        for p in vencidas:
            self.prioridades.eliminar(p)
