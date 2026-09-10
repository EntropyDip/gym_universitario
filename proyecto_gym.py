from dataclasses import dataclass

@dataclass
class Usuario:
    nombre: str
    documento: str
    programa: str

@dataclass
class Reserva:
    documento: str
    nombre_usuario: str
    horario: str
    activa: bool = True

    def cancelar(self) -> str:
            """Marca la reserva como cancelada."""
            if not self.activa:
                return f"La reserva de {self.nombre_usuario} ya estaba cancelada."
            self.activa = False
            return f"Reserva de {self.nombre_usuario} a las {self.horario} cancelada."
    
    def confirmar(self) -> str:
            """Se reactiva una reserva previamente cancelada."""
            if self.activa:
                return f"La reserva de {self.nombre_usuario} ya está activa."
            self.activa = True
            return f"Reserva de {self.nombre_usuario} confirmada nuevamente para las {self.horario}."

    def coincide_con(self, documento: str) -> bool:
        """Verificamos si esta reserva pertenece a un documento dado."""
        return self.documento == documento

    def mostrar_resumen(self) -> str:
        """Se devuelve un texto legible con los datos de la reserva."""
        estado = "activa" if self.activa else "cancelada"
        return f"Reserva ({estado}) — {self.nombre_usuario} ({self.documento}) a las {self.horario}"

class Gym:
    def __init__(self, nombre: str, tiempo_maximo: str = "1:30 horas") -> None:
        self.name = nombre
        self.usuarios: list[Usuario] = []
        self.horarios_disponibles: list[str] = ["08:00 AM", "10:00 AM", "02:00 PM"]
        self.tiempo_maximo = tiempo_maximo
        self.reservas: dict[str, str] = {}
        self.registros: list[dict] = []

    def registrar_usuario(self, nombre:str, documento:str, programa: str) -> str:
        for u in self.usuarios:
            if u.documento  == documento:
                return f"el documento {documento} ya se encuentra registrado"

        nuevo_usuario = Usuario(nombre, documento, programa)
        self.usuarios.append(nuevo_usuario)
        return f"Usuario {nombre} registrado exitosamente."

    def cancelar_registro(self, nombre:str, documento:str) -> str:
        for usuario in self.usuarios:
            if usuario.nombre == nombre and usuario.documento == documento:
                self.usuarios.remove(usuario)
                return f"el usuario {nombre} cancelo la reserva de forma exitosa"

    def realizar_reserva(self, documento: str, horario_deseado: str) -> str:
        usuario_encontrado = False
        nombre_usuario = ""

        for u in self.usuarios:
            if u.documento == documento:
                usuario_encontrado = True
                nombre_usuario = u.nombre
                break

        if not usuario_encontrado:
            return f"Error: El documento {documento} no está registrado para hacer la reserva"

        if horario_deseado not in self.horarios_disponibles:
            agenda_formateada = " | ".join(self.horarios_disponibles)
            return (f"El horario '{horario_deseado}' no existe.\n"
                    f"Horarios disponibles: {agenda_formateada}\n"
                    f"Tiempo máximo permitido por sesión: {self.tiempo_maximo}.")

        self.reservas[documento] = horario_deseado
        return f"¡Reserva exitosa! {nombre_usuario} tiene su espacio a las {horario_deseado}. el tiempo para estar haciendo uso del gym es: {self.tiempo_maximo}."
    
    def registrar_visita(self, documento: str, horario: str,  duracion: int, equipos: list[str]) -> str:
        usuario_encontrado = any(u.documento == documento for u in self.usuarios)
    
        if not usuario_encontrado:
            return "El usuario no está registrado."
    
        registro = {"documento": documento, "horario": horario,"duracion": duracion, "equipos": equipos}
    
        self.registros.append(registro)
    
        return "Visita registrada correctamente."
    
    def horario_mas_frecuente(self) -> str:
    
        if not self.registros:
            return "No hay visitas registradas."
    
        horarios = [registro["horario"] for registro in self.registros]
    
        horario = max(set(horarios), key=horarios.count)
    
        return f"El horario más frecuente es {horario}."
    
    def programa_mas_frecuente(self) -> str:
    
        if not self.usuarios:
            return "No hay usuarios registrados."
    
        programas = [usuario.programa for usuario in self.usuarios]
    
        carrera = max(set(programas), key=programas.count)
    
        return f"La carrera más frecuente es {carrera}."

if __name__ == "__main__":
    mi_gym = Gym("Gimnasio Universidad")
    mi_gym.registrar_usuario("Juan Jose", "1001")

    # Intento con una hora incorrecta para ver la agenda
    print(mi_gym.realizar_reserva("1001", "07:00 AM"))
    print("-" * 40)

    # Reserva exitosa (ejemplo: bloque para rutina de jalón/empuje)
    print(mi_gym.realizar_reserva("1001", "10:00 AM"))
