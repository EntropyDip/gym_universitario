from dataclasses import dataclass
from datetime import datetime, timedelta

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
        self.usuarios: dict[str, Usuario] = {}
        self.horarios_disponibles: list[str] = ["08:00 AM", "10:00 AM", "02:00 PM"]
        self.tiempo_maximo = tiempo_maximo
        self.reservas: list[Reserva] = []
        self.registros: list[dict] = []
        self.prioridades: list[dict] = []


    def registrar_usuario(self, nombre: str, documento: str, programa: str) -> str:
    # Registra un nuevo usuario verificando que su documento no esté repetido.
        if documento in self.usuarios:
            return f"el documento {documento} ya se encuentra registrado"
        nuevo_usuario = Usuario(nombre, documento, programa)
        self.usuarios[documento] = nuevo_usuario
        return f"Usuario {nombre} registrado exitosamente."

    def eliminar_usuario(self, nombre:str, documento:str) -> str:
    # Elimina un usuario del gimnasio usando su nombre y documento.
        if documento in self.usuarios and self.usuarios[documento].nombre == nombre:
            self.usuarios.pop(documento)
            return f"el usuario identificado con {documento} se eliminó correctamente"
        return "El usuario no está registrado"


    def realizar_reserva(self, documento: str, horario_deseado: str, fecha: str) -> str:
        if documento not in self.usuarios:
            return f"Error: El documento {documento} no está registrado para hacer la reserva"

        nombre_usuario = self.usuarios[documento].nombre

        if horario_deseado not in self.horarios_disponibles:
            agenda_formateada = " | ".join(self.horarios_disponibles)
            return (f"El horario '{horario_deseado}' no existe.\n"
                    f"Horarios disponibles: {agenda_formateada}\n"
                    f"Tiempo máximo permitido por sesión: {self.tiempo_maximo}.")

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
