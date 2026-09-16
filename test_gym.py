# -----------------------------------------------------------------
# Pruebas manuales para el sistema del gimnasio.
# -----------------------------------------------------------------
from datetime import datetime
from proyecto_gym import Gym, Usuario, Reserva

hora_actual = datetime(2025, 6, 10, 6, 0)  # hora fija para las pruebas de reserva/prioridad

pruebas_totales = 0
pruebas_ok = 0


def verificar(nombre_prueba: str, obtenido, esperado):
    """Compara lo que devolvió tu código contra lo que debería devolver."""
    global pruebas_totales, pruebas_ok
    pruebas_totales += 1
    if obtenido == esperado:
        pruebas_ok += 1
        print(f"[OK] {nombre_prueba}")
    else:
        print(f"[FALLÓ] {nombre_prueba}")
        print(f"        esperado : {esperado!r}")
        print(f"        obtenido : {obtenido!r}")


# ===================================================================
# 1. REGISTRO DE USUARIOS
# ===================================================================
print("\n--- registrar_usuario ---")
gym = Gym("Gimnasio de Pruebas")

verificar(
    "registrar usuario nuevo",
    gym.registrar_usuario("Ana Ruiz", "100", "Ingeniería de Sistemas"),
    "usuario Ana Ruiz registrado exitosamente."
)

verificar(
    "registrar el mismo documento otra vez debe fallar",
    gym.registrar_usuario("Ana Ruiz Otra Vez", "100", "Ingeniería de Sistemas"),
    "el documento 100 ya se encuentra registrado"
)

verificar(
    "el usuario duplicado no debe sobrescribir al original",
    gym.usuarios["100"].nombre,
    "Ana Ruiz"
)

# ===================================================================
# 2. ELIMINAR USUARIO
# ===================================================================
print("\n--- eliminar_usuario ---")
gym.registrar_usuario("Luis Pérez", "200", "Ingeniería Industrial")

verificar(
    "eliminar con nombre incorrecto no debe borrar nada",
    gym.eliminar_usuario("Nombre Que No Es", "200"),
    "El usuario no está registrado"
)
verificar(
    "el usuario sigue existiendo tras el intento fallido",
    "200" in gym.usuarios,
    True
)

verificar(
    "eliminar documento que no existe",
    gym.eliminar_usuario("Nadie", "999"),
    "El usuario no está registrado"
)

verificar(
    "eliminar usuario correctamente",
    gym.eliminar_usuario("Luis Pérez", "200"),
    "El usuario identificado con 200 se eliminó correctamente."
)
verificar(
    "el usuario ya no debe existir tras eliminarlo",
    "200" in gym.usuarios,
    False
)

# ===================================================================
# 3. REALIZAR RESERVA
# ===================================================================
print("\n--- realizar_reserva ---")

verificar(
    "reservar con documento no registrado",
    gym.realizar_reserva("777", "08:00 AM", "2025-06-10", hora_actual),
    "Error: El documento 777 no está registrado para hacer la reserva"
)

verificar(
    "reservar en un horario que no existe",
    gym.realizar_reserva("100", "07:00 AM", "2025-06-10", hora_actual),
    "El horario '07:00 AM' no existe.\n"
    "Horarios disponibles: 08:00 AM | 10:00 AM | 02:00 PM\n"
    "Tiempo máximo permitido por sesión: 1:30 horas."
)

verificar(
    "reserva exitosa",
    gym.realizar_reserva("100", "08:00 AM", "2025-06-10", hora_actual),
    "¡Reserva exitosa! Ana Ruiz tiene su espacio a las 08:00 AM. "
    "el tiempo para estar haciendo uso del gym es: 1:30 horas."
)

verificar(
    "no debe poder reservar dos veces el mismo día",
    gym.realizar_reserva("100", "10:00 AM", "2025-06-10", hora_actual),
    "El usuario Ana Ruiz ya tiene una reserva activa."
)

verificar(
    "sí debe poder reservar otro día",
    gym.realizar_reserva("100", "10:00 AM", "2025-06-11", hora_actual),
    "¡Reserva exitosa! Ana Ruiz tiene su espacio a las 10:00 AM. "
    "el tiempo para estar haciendo uso del gym es: 1:30 horas."
)

verificar(
    "deben existir 2 reservas activas en total",
    len(gym.reservas),
    2
)

# ===================================================================
# 4. REGISTRAR VISITA
# ===================================================================
print("\n--- registrar_visita ---")

verificar(
    "registrar visita con documento no registrado",
    gym.registrar_visita("777", "08:00 AM", 60, ["caminadora"]),
    "El usuario no está registrado."
)

verificar(
    "registrar visita exitosa",
    gym.registrar_visita("100", "08:00 AM", 60, ["caminadora", "pesas"]),
    "Visita registrada correctamente."
)

gym.registrar_usuario("Marta Gil", "300", "Psicología")
gym.registrar_visita("300", "08:00 AM", 45, ["bicicleta"])
gym.registrar_visita("300", "10:00 AM", 30, ["pesas"])

# ===================================================================
# 5. HORARIO MÁS FRECUENTE
# ===================================================================
print("\n--- horario_mas_frecuente ---")

gym_vacio = Gym("Gimnasio Vacío")
verificar(
    "sin visitas registradas",
    gym_vacio.horario_mas_frecuente(),
    "No hay visitas registradas."
)

verificar(
    "horario más frecuente con datos (08:00 AM aparece 2 veces)",
    gym.horario_mas_frecuente(),
    "El horario más frecuente es 08:00 AM."
)

# ===================================================================
# 6. PROGRAMA MÁS FRECUENTE
# ===================================================================
print("\n--- programa_mas_frecuente ---")

verificar(
    "sin usuarios registrados",
    gym_vacio.programa_mas_frecuente(),
    "No hay usuarios registrados."
)

gym.registrar_usuario("Pedro Soto", "400", "Ingeniería de Sistemas")
verificar(
    "programa más frecuente con datos (Ing. de Sistemas x2)",
    gym.programa_mas_frecuente(),
    "La carrera más frecuente es Ingeniería de Sistemas."
)

# ===================================================================
# 7. MÉTODOS DE LA CLASE Reserva (independientes de Gym)
# ===================================================================
print("\n--- métodos de Reserva ---")

r = Reserva("500", "Sofía León", "02:00 PM", "2025-07-01")

verificar("una reserva nueva empieza activa", r.activa, True)
verificar("coincide_con con el documento correcto", r.coincide_con("500"), True)
verificar("coincide_con con un documento distinto", r.coincide_con("999"), False)

verificar(
    "cancelar una reserva activa",
    r.cancelar(),
    "Reserva de Sofía León a las 02:00 PM cancelada."
)
verificar(
    "cancelar una reserva que ya estaba cancelada",
    r.cancelar(),
    "La reserva de Sofía León ya estaba cancelada."
)
verificar(
    "confirmar una reserva cancelada la reactiva",
    r.confirmar(),
    "Reserva de Sofía León confirmada nuevamente para las 02:00 PM."
)
verificar(
    "confirmar una reserva que ya estaba activa",
    r.confirmar(),
    "La reserva de Sofía León ya está activa."
)
verificar(
    "mostrar_resumen con la reserva activa",
    r.mostrar_resumen(),
    "Reserva (activa) — Sofía León (500) a las 02:00 PM"
)

# ===================================================================
# 8. VALIDACIONES DEL __post_init__ (deben lanzar ValueError)
# ===================================================================
print("\n--- validaciones de datos vacíos ---")

try:
    Usuario("", "600", "Derecho")
    print("[FALLÓ] debía lanzar ValueError con nombre vacío")
    pruebas_totales += 1
except ValueError:
    print("[OK] nombre vacío lanza ValueError")
    pruebas_ok += 1
    pruebas_totales += 1

try:
    Reserva("   ", "Nombre", "08:00 AM", "2025-06-10")
    print("[FALLÓ] debía lanzar ValueError con documento vacío")
    pruebas_totales += 1
except ValueError:
    print("[OK] documento vacío en Reserva lanza ValueError")
    pruebas_ok += 1
    pruebas_totales += 1

# ===================================================================
# RESUMEN FINAL
# ===================================================================
print("\n" + "=" * 50)
print(f"RESULTADO: {pruebas_ok}/{pruebas_totales} pruebas pasaron")
print("=" * 50)
