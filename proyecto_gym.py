from dataclasses import dataclass
from datetime import datetime, timedelta

min_visitas_habitual = 3
horas_limite_confirmacion = 2

def es_bisiesto(anio: int) -> bool:
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)

def es_fecha_valida(fecha: str) -> bool:
    partes = fecha.split("-")
    if len(partes) != 3:
        return False

    anio_texto, mes_texto, dia_texto = partes
    if not (anio_texto.isdigit() and mes_texto.isdigit() and dia_texto.isdigit()):
        return False
    if len(anio_texto) != 4 or len(mes_texto) != 2 or len(dia_texto) != 2:
        return False

    anio, mes, dia = int(anio_texto), int(mes_texto), int(dia_texto)
    if not 1 <= mes <= 12:
        return False

    # Días que tiene cada mes (febrero se ajusta si el año es bisiesto).
    dias_por_mes = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    maximo_dia = dias_por_mes[mes - 1]
    if mes == 2 and not es_bisiesto(anio):
        maximo_dia = 28

    return 1 <= dia <= maximo_dia

@dataclass
class Usuario:
# Representa a un usuario del gimnasio y guarda sus datos personales y académicos.
    nombre: str
    documento: str
    programa: str

    def __post_init__(self):
        if not self.nombre.strip():
            raise ValueError("El nombre no puede quedar vacío")
        if not self.documento.strip():
            raise ValueError("El documento no puede estar vacio")
        if not self.programa.strip():
            raise ValueError("El programa académico no puede quedar vacío")
@dataclass
class Reserva:
# Representa una reserva del gimnasio y almacena sus datos y estado.
    documento: str
    nombre_usuario: str
    horario: str
    fecha: str 
    activa: bool = True

    def __post_init__(self):
        if not self.documento.strip():
            raise ValueError("El documento no pued estar vacío")
        if not es_fecha_valida(self.fecha):
            raise ValueError("La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15")

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

@dataclass
class Visita:
    # Representa una visita de un usuario al gimnasio: horario, duración y equipos usados.
    documento: str
    horario: str
    duracion: int
    equipos: list[str]
    
    def __post_init__(self):
        if self.duracion <= 0:
            raise ValueError("La duración debe ser un número positivo de minutos")
        self.equipos = list(self.equipos)
        
@dataclass
class Prioridad:
    # Representa un cupo apartado con prioridad para un usuario en un horario y fecha.
    documento: str
    nombre: str
    horario: str
    fecha: str
    confirmada: bool = False
    
class Gym:
# Gestiona usuarios, reservas, visitas y horarios del gimnasio.
    def __init__(self, nombre: str, tiempo_maximo: str = "1:30 horas") -> None:
# Inicializa el gimnasio con su nombre, horarios, usuarios y registros.
        self.nombre = nombre
        self.usuarios: dict[str, Usuario] = {}
        self.horarios_disponibles: list[str] = ["08:00 AM", "10:00 AM", "02:00 PM"]
        self.tiempo_maximo = tiempo_maximo
        self.reservas: list[Reserva] = []
        self.registros: list[Visita] = []
        self.prioridades: list[Prioridad] = []


    def registrar_usuario(self, nombre: str, documento: str, programa: str) -> str:
    # Registra un nuevo usuario verificando que su documento no esté repetido.
        if documento in self.usuarios:
            return f"El documento {documento} ya se encuentra registrado"
        nuevo_usuario = Usuario(nombre, documento, programa)
        self.usuarios[documento] = nuevo_usuario
        return f"Usuario {nombre} registrado exitosamente."

    def eliminar_usuario(self, nombre:str, documento:str) -> str:
    # Elimina un usuario del gimnasio usando su nombre y documento.
        if documento not in self.usuarios or self.usuarios[documento].nombre != nombre:
            return "El usuario no está registrado"

        self.usuarios.pop(documento)
        self.reservas = self._quitar_por_documento(self.reservas, documento)
        self.registros = self._quitar_por_documento(self.registros, documento)
        self.prioridades = self._quitar_por_documento(self.prioridades, documento)
        return f"El usuario identificado con {documento} se eliminó correctamente."

    def _quitar_por_documento(self, lista: list, documento: str) -> list:
        resultado = []
        for elemento in lista:
            if elemento.documento != documento:
                resultado.append(elemento)
        return resultado
        
    def realizar_reserva(self, documento: str, horario_deseado: str, fecha: str, hora_actual: datetime) -> str:
    # Reserva un horario validando
    # documento, fecha, horario y el respeto a las prioridades ya otorgadas.   
        if documento not in self.usuarios:
            return f"Error: El documento {documento} no está registrado para hacer la reserva"

        if not es_fecha_valida(fecha):
            return "Error: La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15."
        
        self._liberar_prioridades_vencidas(hora_actual)   
        nombre_usuario = self.usuarios[documento].nombre

        if horario_deseado not in self.horarios_disponibles:
            agenda_formateada = " | ".join(self.horarios_disponibles)
            return (f"El horario '{horario_deseado}' no existe.\n"
                    f"Horarios disponibles: {agenda_formateada}\n"
                    f"Tiempo máximo permitido por sesión: {self.tiempo_maximo}.")
        
        for prioridad in self.prioridades:
            if prioridad.horario == horario_deseado and prioridad.fecha == fecha:
                if prioridad.documento != documento:
                    return (f"El horario {horario_deseado} del {fecha} está apartado "
                            f"con prioridad para {prioridad.nombre}.")
                return (f"{nombre_usuario} ya tiene este horario apartado con prioridad. "
                        f"No es necesario hacer otra reserva.")
                
        for reserva in self.reservas:
            if reserva.documento == documento and reserva.fecha == fecha and reserva.activa:
                return f"El usuario {nombre_usuario} ya tiene una reserva activa."

        nueva_reserva = Reserva(documento, nombre_usuario, horario_deseado, fecha)
        self.reservas.append(nueva_reserva)
        
        return f"¡Reserva exitosa! {nombre_usuario} tiene su espacio a las {horario_deseado}. el tiempo para estar haciendo uso del gym es: {self.tiempo_maximo}."
    
    def registrar_visita(self, documento: str, horario: str,  duracion: int, equipos: list[str]) -> str:
# Registra una visita indicando horario, duración y equipos utilizados.
        if documento not in self.usuarios:
            return "El usuario no está registrado."
    
        if horario not in self.horarios_disponibles:
            return (f"Error: El horario '{horario}' no existe. "
                    f"Disponibles: {' | '.join(self.horarios_disponibles)}.")

        registro = Visita(documento, horario, duracion, equipos)
        self.registros.append(registro)
        return "Visita registrada correctamente."
    
    def horario_mas_frecuente(self) -> str:
# Determina el horario en el que se registran más visitas al gimnasio.
        if not self.registros:
            return "No hay visitas registradas."
    
        conteo = {}

        for registro in self.registros:
            horario = registro.horario
    
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
        if not self.usuarios:
            return "No hay usuarios registrados."

        conteo = {}
        for usuario in self.usuarios.values():
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
# Calcula  para cada usuario que tiene visitas registradas, el promedio de duración.
        if not self.registros:
            return "No hay visitas registradas."

        suma_por_usuario = {}
        cantidad_por_usuario = {}

        for registro in self.registros:
            doc = registro.documento
            duracion = registro.duracion

            if doc not in suma_por_usuario:
                suma_por_usuario[doc] = 0
                cantidad_por_usuario[doc] = 0

            suma_por_usuario[doc] += duracion
            cantidad_por_usuario[doc] += 1

        resultado = "Promedio de duración por usuario:\n"

        for doc in suma_por_usuario:
            promedio = suma_por_usuario[doc] / cantidad_por_usuario[doc]

            nombre = doc
            for u in self.usuarios.values():
                if u.documento == doc:
                    nombre = u.nombre
                    break

            resultado += f"- {nombre} ({doc}): {promedio:.1f} minutos en promedio\n"

        return resultado

    def prioridad_membresia(self, documento: str, horario: str, fecha: str, hora_actual: datetime) -> str:
# Da prioridad exclusiva a un usuario para reservar un horario, si es "habitual" ahí
# (ha ido varias veces a esa misma hora) o si tiene más tiempo acumulado en el gimnasio
# que los demás usuarios.
        if documento not in self.usuarios:
            return "El usuario no está registrado."

        if horario not in self.horarios_disponibles:
            return (f"Error: El horario '{horario}' no existe. "
                    f"Disponibles: {' | '.join(self.horarios_disponibles)}.")

        if not es_fecha_valida(fecha):
            return "Error: La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15."

        usuario = self.usuarios[documento]

        self._liberar_prioridades_vencidas(hora_actual)
        
        for prioridad in self.prioridades:
            if prioridad.horario == horario and prioridad.fecha == fecha:
                if prioridad.documento == documento:
                    return f"{usuario.nombre} ya tiene prioridad para el horario {horario} del {fecha}."
                return (f"El horario {horario} del {fecha} ya está apartado "
                        f"con prioridad por {prioridad.nombre}.")

        veces_en_ese_horario = 0
        for visita in self.registros:
            if visita.documento == documento and visita.horario == horario:
                veces_en_ese_horario += 1
        es_habitual = veces_en_ese_horario >= min_visitas_habitual

        tiempo_por_usuario = {}
        for visita in self.registros:
            doc = visita.documento
            if doc not in tiempo_por_usuario:
                tiempo_por_usuario[doc] = 0
            tiempo_por_usuario[doc] += visita.duracion

        # .get(clave, 0) devuelve 0 si el usuario no tiene visitas registradas.
        tiempo_usuario = tiempo_por_usuario.get(documento, 0)

        tiene_mas_tiempo = tiempo_usuario > 0
        for doc in tiempo_por_usuario:
            if doc != documento and tiempo_por_usuario[doc] > tiempo_usuario:
                tiene_mas_tiempo = False

        if not es_habitual and not tiene_mas_tiempo:
            return f"{usuario.nombre} no cumple los requisitos para tener prioridad en el horario {horario}."

        # CAMBIADO: antes se creaba un diccionario; ahora se usa la dataclass Prioridad.
        self.prioridades.append(Prioridad(documento, usuario.nombre, horario, fecha))

        return (f"{usuario.nombre} obtuvo prioridad para el horario {horario} del {fecha}. "
                f"Tiene hasta 2 horas antes para confirmar asistencia con confirmar_prioridad().")

    def confirmar_prioridad(self, documento: str, horario: str, fecha: str, hora_actual: datetime) -> str:
# Confirma (o libera) una prioridad. Si se confirma antes del límite de 2 horas antes
# del horario, el cupo queda exclusivo. Si ya pasó ese límite, el cupo se libera solo.
        if not self.prioridades:
            return "No hay prioridades registradas."
            
        for prioridad in self.prioridades:
            if (prioridad.documento == documento and prioridad.horario == horario and prioridad.fecha == fecha):
                        
                if prioridad.confirmada:
                    return (f"{prioridad.nombre} ya había confirmado el cupo "
                            f"de las {horario} del {fecha}.")
                hora_del_horario = datetime.strptime(f"{fecha} {horario}", "%Y-%m-%d %I:%M %p")
                limite_para_confirmar = hora_del_horario - timedelta(hours=horas_limite_confirmacion)

                if hora_actual > limite_para_confirmar:
                            self.prioridades.remove(prioridad)
                            return (f"{prioridad.nombre} no confirmó a tiempo, "
                                    f"el cupo de las {horario} del {fecha} queda libre.")
        
                prioridad.confirmada = True
                return (f"{prioridad.nombre} confirmó su asistencia, "
                                f"el cupo de las {horario} del {fecha} es exclusivo.")

        return "No se encontró una prioridad con esos datos."

    def _liberar_prioridades_vencidas(self, hora_actual: datetime) -> None:
            vencidas = []
            for prioridad in self.prioridades:
                if not prioridad.confirmada:
                    hora_del_horario = datetime.strptime(
                        f"{prioridad.fecha} {prioridad.horario}", "%Y-%m-%d %I:%M %p")
                    limite = hora_del_horario - timedelta(hours=horas_limite_confirmacion)
                    if hora_actual > limite:
                        vencidas.append(prioridad)
    
            for prioridad in vencidas:
                self.prioridades.remove(prioridad)
