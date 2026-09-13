from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Usuario:
# Representa a un usuario del gimnasio y guarda sus datos personales y académicos.
    nombre: str
    documento: str
    programa: str

@dataclass
class Reserva:
# Representa una reserva del gimnasio y almacena sus datos y estado.
    documento: str
    nombre_usuario: str
    horario: str
    fecha: str 
    activa: bool = True
    prioritaria: bool = False   # True si la reserva se hizo con prioridad de membresía
    confirmada: bool = False    # True si el usuario confirmó asistencia dentro del plazo

    def cancelar(self) -> str:
# Cancela una reserva activa y actualiza su estado.        
        if not self.activa:
            return f"La reserva de {self.nombre_usuario} ya estaba cancelada."
        self.activa = False
        return f"Reserva de {self.nombre_usuario} a las {self.horario} cancelada."
    
    def confirmar(self) -> str:
# Reactiva una reserva que había sido cancelada.
        if self.activa:
            return f"La reserva de {self.nombre_usuario} ya está activa."
        self.activa = True
        return f"Reserva de {self.nombre_usuario} confirmada nuevamente para las {self.horario}."

    def coincide_con(self, documento: str) -> bool:
# Comprueba si la reserva pertenece al documento indicado.
        return self.documento == documento

    def mostrar_resumen(self) -> str:
 # Muestra de forma resumida los datos y estado de la reserva.
        estado = "activa" if self.activa else "cancelada"
        return f"Reserva ({estado}) — {self.nombre_usuario} ({self.documento}) a las {self.horario}"

class Gym:
# Gestiona usuarios, reservas, visitas y horarios del gimnasio.
    def __init__(self, nombre: str, tiempo_maximo: str = "1:30 horas") -> None:
# Inicializa el gimnasio con su nombre, horarios, usuarios y registros.
        self.name = nombre
        self.usuarios: list[Usuario] = []
        self.horarios_disponibles: list[str] = ["08:00 AM", "10:00 AM", "02:00 PM"]
        self.tiempo_maximo = tiempo_maximo
        self.reservas: list[Reserva] = []
        self.registros: list[dict] = []

    def registrar_usuario(self, nombre: str, documento: str, programa: str) -> str:
# Registra un nuevo usuario verificando que su documento no esté repetido.
        for u in self.usuarios:
            if u.documento  == documento:
                return f"el documento {documento} ya se encuentra registrado"

        nuevo_usuario = Usuario(nombre, documento, programa)
        self.usuarios.append(nuevo_usuario)
        return f"Usuario {nombre} registrado exitosamente."

    def eliminar_usuario(self, nombre:str, documento:str) -> str:
# Elimina un usuario del gimnasio usando su nombre y documento.
        for usuario in self.usuarios:
            if usuario.nombre == nombre and usuario.documento == documento:
                self.usuarios.remove(usuario)
                return f"el usuario {nombre} fue eliminado correctamente"
                
        return "El usuario no está registrado"

    def _fecha_hora_reserva(self, reserva: Reserva) -> datetime:
# Convierte la fecha y el horario (texto) de una reserva en un objeto datetime real.
        return datetime.strptime(f"{reserva.fecha} {reserva.horario}", "%Y-%m-%d %I:%M %p")

    def _horario_bloqueado_por_prioridad(self, horario: str, fecha: str, documento: str, momento_actual: datetime) -> str | None:
# Revisa si ya existe una reserva prioritaria de OTRO usuario que bloquee ese horario.
# Retorna un mensaje de bloqueo si aplica, o None si el horario está libre para reservar.
        for reserva in self.reservas:
            if (reserva.horario == horario and reserva.fecha == fecha
                    and reserva.activa and reserva.prioritaria and reserva.documento != documento):
                hora_reserva = self._fecha_hora_reserva(reserva)
                limite_confirmacion = hora_reserva - timedelta(hours=2)
                # Si ya confirmó, el cupo es exclusivo sin importar la hora.
                if reserva.confirmada:
                    return f"El horario {horario} del {fecha} está reservado con exclusividad por {reserva.nombre_usuario}."
                # Si aún no se llega al límite de 2 horas antes, el cupo sigue apartado para el usuario prioritario.
                if momento_actual < limite_confirmacion:
                    return (f"El horario {horario} del {fecha} está apartado con prioridad para "
                            f"{reserva.nombre_usuario} hasta {limite_confirmacion.strftime('%Y-%m-%d %I:%M %p')}.")
        return None

    def realizar_reserva(self, documento: str, horario_deseado: str, fecha: str, momento_actual: datetime | None = None) -> str:
# Permite reservar un horario disponible para un usuario registrado.
        usuario_encontrado = False
        nombre_usuario = ""

        for u in self.usuarios:
            if u.documento == documento:
                usuario_encontrado = True
                nombre_usuario = u.nombre
                break

        if not usuario_encontrado:
            return f"Error: El documento {documento} no está registrado para hacer la reserva"

        for reserva in self.reservas:
            if reserva.documento == documento and reserva.fecha == fecha and reserva.activa:
                return f"El usuario {nombre_usuario} ya tiene una reserva activa."
        
        if horario_deseado not in self.horarios_disponibles:
            agenda_formateada = " | ".join(self.horarios_disponibles)
            return (f"El horario '{horario_deseado}' no existe.\n"
                    f"Horarios disponibles: {agenda_formateada}\n"
                    f"Tiempo máximo permitido por sesión: {self.tiempo_maximo}.")

        # Si se indica el momento actual, se respeta la exclusividad de las reservas prioritarias.
        if momento_actual is not None:
            bloqueo = self._horario_bloqueado_por_prioridad(horario_deseado, fecha, documento, momento_actual)
            if bloqueo:
                return bloqueo
            
        nueva_reserva = Reserva(documento, nombre_usuario, horario_deseado, fecha)
        self.reservas.append(nueva_reserva)
        
        return f"¡Reserva exitosa! {nombre_usuario} tiene su espacio a las {horario_deseado}. el tiempo para estar haciendo uso del gym es: {self.tiempo_maximo}."
    
    def registrar_visita(self, documento: str, horario: str,  duracion: int, equipos: list[str]) -> str:
# Registra una visita indicando horario, duración y equipos utilizados.
        usuario_encontrado = False 
        for u in self.usuarios: 
            if u.documento == documento: 
                usuario_encontrado = True 
                break
        if not usuario_encontrado:
            return "El usuario no está registrado."
    
        registro = {"documento": documento, "horario": horario,"duracion": duracion, "equipos": equipos}
    
        self.registros.append(registro)
    
        return "Visita registrada correctamente."
    
    def horario_mas_frecuente(self) -> str:
# Determina el horario en el que se registran más visitas al gimnasio.
        if not self.registros:
            return "No hay visitas registradas."
    
        conteo = {}

        for registro in self.registros:
            horario = registro["horario"]
    
            if horario in conteo:
                conteo[horario] += 1
            else:
                conteo[horario] = 1
    
        horario_frecuente = ""
        mayor = 0
    
        for horario in conteo:
            if conteo[horario] > mayor:
                mayor = conteo[horario]
                horario_frecuente = horario
    
        return f"El horario más frecuente es {horario_frecuente}."
    
    def programa_mas_frecuente(self) -> str:
# Determina el programa académico con más usuarios registrados.    
        if not self.usuarios:
            return "No hay usuarios registrados."
    
        conteo = {}

        for usuario in self.usuarios:
            programa = usuario.programa
    
            if programa in conteo:
                conteo[programa] += 1
            else:
                conteo[programa] = 1
    
        programa_frecuente = ""
        mayor = 0
    
        for programa in conteo:
            if conteo[programa] > mayor:
                mayor = conteo[programa]
                programa_frecuente = programa
        
        return f"La carrera más frecuente es {programa_frecuente}."

    def promedio_duracion_por_usuario(self) -> str:
# Calcula el promedio de duración de las visitas registradas, por cada usuario.
        if not self.registros:
            return "No hay visitas registradas."

        suma_duraciones: dict[str, int] = {}
        cantidad_visitas: dict[str, int] = {}

        for registro in self.registros:
            doc = registro["documento"]
            suma_duraciones[doc] = suma_duraciones.get(doc, 0) + registro["duracion"]
            cantidad_visitas[doc] = cantidad_visitas.get(doc, 0) + 1

        lineas = []
        for doc in suma_duraciones:
            promedio = suma_duraciones[doc] / cantidad_visitas[doc]

            nombre_usuario = doc
            for u in self.usuarios:
                if u.documento == doc:
                    nombre_usuario = u.nombre
                    break

            lineas.append(f"{nombre_usuario} ({doc}): {promedio:.1f} minutos en promedio "
                          f"({cantidad_visitas[doc]} visita(s))")

        return "Promedio de duración por usuario:\n" + "\n".join(lineas)

    def _es_usuario_habitual(self, documento: str, horario: str, minimo_visitas: int = 3) -> bool:
# Un usuario es "habitual" en un horario si ha registrado visitas ahí varias veces.
        visitas_en_horario = 0
        for registro in self.registros:
            if registro["documento"] == documento and registro["horario"] == horario:
                visitas_en_horario += 1
        return visitas_en_horario >= minimo_visitas

    def _tiempo_total_usuario(self, documento: str) -> int:
# Suma la duración total (en minutos) que un usuario ha usado el gimnasio.
        total = 0
        for registro in self.registros:
            if registro["documento"] == documento:
                total += registro["duracion"]
        return total

    def prioridad_membresia(self, documento: str, horario: str, fecha: str) -> str:
# Otorga una reserva prioritaria y exclusiva a un usuario que sea "habitual" en ese
# horario, o que tenga más tiempo acumulado en el gimnasio que el resto de usuarios.
# Esa reserva bloquea el horario para los demás. El usuario tiene hasta 2 horas antes
# del horario para confirmar su asistencia (ver confirmar_asistencia_prioritaria):
# si confirma, el cupo queda exclusivamente para él/ella; si no confirma a tiempo,
# el cupo se libera automáticamente (ver liberar_cupos_no_confirmados).
        usuario_encontrado = None
        for u in self.usuarios:
            if u.documento == documento:
                usuario_encontrado = u
                break

        if usuario_encontrado is None:
            return f"Error: el documento {documento} no está registrado."

        if horario not in self.horarios_disponibles:
            return f"El horario '{horario}' no existe en la agenda del gimnasio."

        es_habitual = self._es_usuario_habitual(documento, horario)

        tiempo_usuario = self._tiempo_total_usuario(documento)
        tiene_mas_tiempo = True
        for otro in self.usuarios:
            if otro.documento != documento and self._tiempo_total_usuario(otro.documento) > tiempo_usuario:
                tiene_mas_tiempo = False
                break

        if not es_habitual and not tiene_mas_tiempo:
            return (f"{usuario_encontrado.nombre} no cumple los requisitos de prioridad por membresía "
                    f"(no es habitual en el horario {horario} ni tiene mayor tiempo acumulado en el gimnasio).")

        for reserva in self.reservas:
            if (reserva.horario == horario and reserva.fecha == fecha
                    and reserva.activa and reserva.prioritaria and reserva.documento != documento):
                return f"El horario {horario} del {fecha} ya tiene una reserva prioritaria de {reserva.nombre_usuario}."

        nueva_reserva = Reserva(documento, usuario_encontrado.nombre, horario, fecha)
        nueva_reserva.prioritaria = True
        self.reservas.append(nueva_reserva)

        return (f"{usuario_encontrado.nombre} obtuvo prioridad de membresía para el horario {horario} "
                f"del {fecha}. Debe confirmar asistencia hasta 2 horas antes; de lo contrario, "
                f"el cupo quedará disponible para otros usuarios.")

    def confirmar_asistencia_prioritaria(self, documento: str, horario: str, fecha: str, momento_actual: datetime) -> str:
# Confirma la asistencia de un usuario con reserva prioritaria, siempre que se haga
# antes del límite de 2 horas previas al horario. Al confirmar, el cupo queda exclusivo.
        for reserva in self.reservas:
            if (reserva.documento == documento and reserva.horario == horario
                    and reserva.fecha == fecha and reserva.prioritaria and reserva.activa):
                hora_reserva = self._fecha_hora_reserva(reserva)
                limite_confirmacion = hora_reserva - timedelta(hours=2)

                if momento_actual > limite_confirmacion:
                    return (f"Ya no se puede confirmar: el límite era "
                            f"{limite_confirmacion.strftime('%Y-%m-%d %I:%M %p')} (2 horas antes del horario).")

                reserva.confirmada = True
                return (f"{reserva.nombre_usuario} confirmó su asistencia. El cupo de las {horario} "
                        f"del {fecha} queda exclusivo para él/ella.")

        return "No se encontró una reserva prioritaria activa con esos datos."

    def liberar_cupos_no_confirmados(self, momento_actual: datetime) -> str:
# Revisa todas las reservas prioritarias sin confirmar cuyo límite de 2 horas ya pasó,
# y libera esos cupos para que cualquier otro usuario pueda reservarlos.
        liberados = []
        for reserva in self.reservas:
            if reserva.prioritaria and reserva.activa and not reserva.confirmada:
                hora_reserva = self._fecha_hora_reserva(reserva)
                limite_confirmacion = hora_reserva - timedelta(hours=2)
                if momento_actual >= limite_confirmacion:
                    reserva.prioritaria = False
                    reserva.activa = False
                    liberados.append(f"{reserva.nombre_usuario} ({reserva.horario} - {reserva.fecha})")

        if not liberados:
            return "No hay cupos prioritarios para liberar en este momento."

        return "Cupos liberados por falta de confirmación: " + ", ".join(liberados)

# Ejecuta ejemplos del sistema cuando el archivo se ejecuta directamente.
if __name__ == "__main__":
    mi_gym = Gym("Gimnasio Universidad")

    # Registro de los 3 estudiantes (todos en Ingeniería de Sistemas)
    print(mi_gym.registrar_usuario("Juan Jose Aguirre", "1001", "Ingeniería de Sistemas"))
    print(mi_gym.registrar_usuario("Samuel Zapata", "1002", "Ingeniería de Sistemas"))
    print(mi_gym.registrar_usuario("Angelina Negrette", "1003", "Ingeniería de Sistemas"))

    # Usuarios adicionales de otros programas
    print(mi_gym.registrar_usuario("Mariana Restrepo", "1004", "Administración de Empresas"))
    print(mi_gym.registrar_usuario("Carlos Herrera", "1005", "Ingeniería Industrial"))
    print(mi_gym.registrar_usuario("Laura Gómez", "1006", "Psicología"))
    print(mi_gym.registrar_usuario("Andrés Torres", "1007", "Ingeniería Financiera"))
    print("-" * 40)

    # Intento con una hora incorrecta para ver la agenda disponible
    print(mi_gym.realizar_reserva("1001", "07:00 AM", "2025-06-10"))
    print("-" * 40)

    # Reservas exitosas para varios usuarios
    print(mi_gym.realizar_reserva("1001", "10:00 AM", "2025-06-10"))
    print(mi_gym.realizar_reserva("1002", "08:00 AM", "2025-06-10"))
    print(mi_gym.realizar_reserva("1003", "02:00 PM", "2025-06-10"))
    print(mi_gym.realizar_reserva("1004", "08:00 AM", "2025-06-10"))
    print(mi_gym.realizar_reserva("1005", "10:00 AM", "2025-06-10"))
    print("-" * 40)

    # Ver el programa más frecuente entre los usuarios registrados
    print(mi_gym.programa_mas_frecuente())
    print("-" * 40)

    # --- Registro de visitas para poder calcular promedios y detectar habituales ---
    print(mi_gym.registrar_visita("1001", "10:00 AM", 60, ["mancuernas"]))
    print(mi_gym.registrar_visita("1001", "10:00 AM", 90, ["banca", "barra"]))
    print(mi_gym.registrar_visita("1001", "10:00 AM", 75, ["cinta"]))
    print(mi_gym.registrar_visita("1002", "08:00 AM", 45, ["cinta"]))
    print("-" * 40)

    # --- Promedio de duración por usuario ---
    print(mi_gym.promedio_duracion_por_usuario())
    print("-" * 40)

    # --- Prioridad por membresía ---
    # 1001 es habitual en el horario de 10:00 AM (3 visitas registradas ahí), así que
    # obtiene prioridad exclusiva para el 2025-06-15.
    print(mi_gym.prioridad_membresia("1001", "10:00 AM", "2025-06-15"))

    # Otro usuario intenta reservar ese mismo horario mientras sigue apartado (falla).
    momento_de_prueba = datetime(2025, 6, 15, 6, 0)  # 6:00 AM, más de 2h antes de las 10:00 AM
    print(mi_gym.realizar_reserva("1002", "10:00 AM", "2025-06-15", momento_de_prueba))

    # 1001 confirma su asistencia antes del límite de 2 horas → cupo queda exclusivo.
    print(mi_gym.confirmar_asistencia_prioritaria("1001", "10:00 AM", "2025-06-15", momento_de_prueba))

    # Simulamos otro caso sin confirmación para ver cómo se libera el cupo.
    print(mi_gym.prioridad_membresia("1001", "08:00 AM", "2025-06-16"))
    momento_limite_pasado = datetime(2025, 6, 16, 6, 30)  # ya pasó el límite de las 6:00 AM
    print(mi_gym.liberar_cupos_no_confirmados(momento_limite_pasado))
    print(mi_gym.realizar_reserva("1002", "08:00 AM", "2025-06-16", momento_limite_pasado))
