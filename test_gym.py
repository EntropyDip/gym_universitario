# -----------------------------------------------------------------
# Pruebas manuales para el sistema del gimnasio.
# -----------------------------------------------------------------
from datetime import datetime
from proyecto_gym import Gym, Usuario, Reserva, Visita, Prioridad, es_fecha_valida, es_bisiesto

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


def verificar_excepcion(nombre_prueba: str, funcion, excepcion_esperada=ValueError):
    """Verifica que 'funcion' (sin argumentos, usa lambda) lance la excepción esperada."""
    global pruebas_totales, pruebas_ok
    pruebas_totales += 1
    try:
        funcion()
        pruebas_ok += 0
        print(f"[FALLÓ] {nombre_prueba}")
        print(f"        esperado : {excepcion_esperada.__name__}")
        print(f"        obtenido : no se lanzó ninguna excepción")
    except excepcion_esperada:
        pruebas_ok += 1
        print(f"[OK] {nombre_prueba}")
    except Exception as e:
        print(f"[FALLÓ] {nombre_prueba}")
        print(f"        esperado : {excepcion_esperada.__name__}")
        print(f"        obtenido : {type(e).__name__}")


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
    "reservar con fecha en formato inválido",
    gym.realizar_reserva("100", "08:00 AM", "10-06-2025", hora_actual),
    "Error: La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2025-06-15."
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
    "registrar visita con horario inexistente",
    gym.registrar_visita("100", "07:00 AM", 60, ["caminadora"]),
    "Error: El horario '07:00 AM' no existe. Disponibles: 08:00 AM | 10:00 AM | 02:00 PM."
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

verificar_excepcion(
    "nombre vacío en Usuario lanza ValueError",
    lambda: Usuario("", "600", "Derecho")
)

verificar_excepcion(
    "documento vacío en Usuario lanza ValueError",
    lambda: Usuario("Nombre", "   ", "Derecho")
)

verificar_excepcion(
    "programa vacío en Usuario lanza ValueError",
    lambda: Usuario("Nombre", "601", "")
)

verificar_excepcion(
    "documento vacío en Reserva lanza ValueError",
    lambda: Reserva("   ", "Nombre", "08:00 AM", "2025-06-10")
)

verificar_excepcion(
    "fecha inválida en Reserva lanza ValueError",
    lambda: Reserva("602", "Nombre", "08:00 AM", "2025-13-01")
)

# ===================================================================
# 9. Visita: validación de duración
# ===================================================================
print("\n--- validaciones de Visita ---")

verificar_excepcion(
    "duración en cero lanza ValueError",
    lambda: Visita("100", "08:00 AM", 0, ["pesas"])
)

verificar_excepcion(
    "duración negativa lanza ValueError",
    lambda: Visita("100", "08:00 AM", -10, ["pesas"])
)

v = Visita("100", "08:00 AM", 30, ["pesas"])
verificar("Visita válida guarda la duración correctamente", v.duracion, 30)
verificar("Visita válida guarda los equipos como lista", v.equipos, ["pesas"])

# ===================================================================
# 10. Prioridad: validaciones
# ===================================================================
print("\n--- validaciones de Prioridad ---")

verificar_excepcion(
    "documento vacío en Prioridad lanza ValueError",
    lambda: Prioridad("", "Nombre", "08:00 AM", "2025-06-10")
)

verificar_excepcion(
    "nombre vacío en Prioridad lanza ValueError",
    lambda: Prioridad("700", "", "08:00 AM", "2025-06-10")
)

verificar_excepcion(
    "fecha inválida en Prioridad lanza ValueError",
    lambda: Prioridad("700", "Nombre", "08:00 AM", "2025-02-30")
)

# ===================================================================
# 11. es_fecha_valida / es_bisiesto
# ===================================================================
print("\n--- es_fecha_valida / es_bisiesto ---")

verificar("2024 es bisiesto", es_bisiesto(2024), True)
verificar("2025 no es bisiesto", es_bisiesto(2025), False)
verificar("1900 no es bisiesto (múltiplo de 100 no de 400)", es_bisiesto(1900), False)
verificar("2000 sí es bisiesto (múltiplo de 400)", es_bisiesto(2000), True)

verificar("fecha válida normal", es_fecha_valida("2025-06-15"), True)
verificar("29 de febrero en año bisiesto es válido", es_fecha_valida("2024-02-29"), True)
verificar("29 de febrero en año NO bisiesto es inválido", es_fecha_valida("2025-02-29"), False)
verificar("mes 13 es inválido", es_fecha_valida("2025-13-01"), False)
verificar("mes 00 es inválido", es_fecha_valida("2025-00-10"), False)
verificar("día 32 es inválido", es_fecha_valida("2025-01-32"), False)
verificar("formato con separador incorrecto es inválido", es_fecha_valida("2025/06/15"), False)
verificar("formato con partes de más es inválido", es_fecha_valida("2025-06-15-00"), False)
verificar("texto no numérico es inválido", es_fecha_valida("aaaa-bb-cc"), False)

# ===================================================================
# 12. promedio_duracion_por_usuario
# ===================================================================
print("\n--- promedio_duracion_por_usuario ---")

gym_prom = Gym("Gimnasio Promedios")
gym_prom.registrar_usuario("Carla Ríos", "800", "Biología")

verificar(
    "sin visitas registradas",
    gym_prom.promedio_duracion_por_usuario(),
    "No hay visitas registradas."
)

gym_prom.registrar_visita("800", "08:00 AM", 40, ["pesas"])
gym_prom.registrar_visita("800", "10:00 AM", 60, ["bicicleta"])

verificar(
    "promedio correcto para un usuario con dos visitas",
    gym_prom.promedio_duracion_por_usuario(),
    "Promedio de duración por usuario:\n- Carla Ríos (800): 50.0 minutos en promedio\n"
)

# ===================================================================
# 13. prioridad_membresia
# ===================================================================
print("\n--- prioridad_membresia ---")

gym_p = Gym("Gimnasio Prioridades")
gym_p.registrar_usuario("Diego Vega", "900", "Física")
gym_p.registrar_usuario("Elena Cruz", "901", "Química")
hora_prioridad = datetime(2025, 6, 10, 6, 0)

verificar(
    "documento no registrado no puede pedir prioridad",
    gym_p.prioridad_membresia("999", "08:00 AM", "2025-06-15", hora_prioridad),
    "El usuario no está registrado."
)

verificar(
    "horario inexistente no puede pedir prioridad",
    gym_p.prioridad_membresia("900", "07:00 AM", "2025-06-15", hora_prioridad),
    "Error: El horario '07:00 AM' no existe. Disponibles: 08:00 AM | 10:00 AM | 02:00 PM."
)

verificar(
    "sin visitas ni tiempo acumulado no cumple los requisitos",
    gym_p.prioridad_membresia("900", "08:00 AM", "2025-06-15", hora_prioridad),
    "Diego Vega no cumple los requisitos para tener prioridad en el horario 08:00 AM."
)

# Diego se vuelve "habitual" en 08:00 AM (3 visitas a esa hora).
gym_p.registrar_visita("900", "08:00 AM", 30, ["pesas"])
gym_p.registrar_visita("900", "08:00 AM", 30, ["pesas"])
gym_p.registrar_visita("900", "08:00 AM", 30, ["pesas"])

verificar(
    "usuario habitual (≥3 visitas en ese horario) obtiene prioridad",
    gym_p.prioridad_membresia("900", "08:00 AM", "2025-06-15", hora_prioridad),
    "Diego Vega obtuvo prioridad para el horario 08:00 AM del 2025-06-15. "
    "Tiene hasta 2 horas antes para confirmar asistencia con confirmar_prioridad()."
)

verificar(
    "pedir la misma prioridad otra vez no la duplica",
    gym_p.prioridad_membresia("900", "08:00 AM", "2025-06-15", hora_prioridad),
    "Diego Vega ya tiene prioridad para el horario 08:00 AM del 2025-06-15."
)

verificar(
    "otro usuario no puede pedir prioridad sobre un horario ya apartado",
    gym_p.prioridad_membresia("901", "08:00 AM", "2025-06-15", hora_prioridad),
    "El horario 08:00 AM del 2025-06-15 ya está apartado con prioridad por Diego Vega."
)

verificar(
    "el horario con prioridad ajena no se puede reservar",
    gym_p.realizar_reserva("901", "08:00 AM", "2025-06-15", hora_prioridad),
    "El horario 08:00 AM del 2025-06-15 está apartado con prioridad para Diego Vega."
)

verificar(
    "el dueño de la prioridad no necesita reservar aparte",
    gym_p.realizar_reserva("900", "08:00 AM", "2025-06-15", hora_prioridad),
    "Diego Vega ya tiene este horario apartado con prioridad. No es necesario hacer otra reserva."
)

# Empate de tiempo acumulado: Elena iguala el tiempo de Diego (90 min cada uno)
# en un horario distinto, donde Diego no es habitual: no debe obtener prioridad.
gym_p.registrar_visita("901", "10:00 AM", 90, ["bicicleta"])
verificar(
    "en caso de empate de tiempo acumulado, nadie tiene prioridad por tiempo",
    gym_p.prioridad_membresia("900", "10:00 AM", "2025-06-16", hora_prioridad),
    "Diego Vega no cumple los requisitos para tener prioridad en el horario 10:00 AM."
)

# ===================================================================
# 14. confirmar_prioridad
# ===================================================================
print("\n--- confirmar_prioridad ---")

gym_c = Gym("Gimnasio Confirmaciones")
gym_c.registrar_usuario("Fabián Ortiz", "950", "Matemáticas")
gym_c.registrar_visita("950", "02:00 PM", 30, ["pesas"])
gym_c.registrar_visita("950", "02:00 PM", 30, ["pesas"])
gym_c.registrar_visita("950", "02:00 PM", 30, ["pesas"])

verificar(
    "sin prioridades registradas",
    gym_c.confirmar_prioridad("950", "02:00 PM", "2025-06-20", datetime(2025, 6, 20, 6, 0)),
    "No hay prioridades registradas."
)

gym_c.prioridad_membresia("950", "02:00 PM", "2025-06-20", datetime(2025, 6, 20, 6, 0))

verificar(
    "confirmar prioridad inexistente (otros datos)",
    gym_c.confirmar_prioridad("950", "08:00 AM", "2025-06-20", datetime(2025, 6, 20, 6, 0)),
    "No se encontró una prioridad con esos datos."
)

verificar(
    "confirmar a tiempo (más de 2 horas antes) deja el cupo exclusivo",
    gym_c.confirmar_prioridad("950", "02:00 PM", "2025-06-20", datetime(2025, 6, 20, 11, 0)),
    "Fabián Ortiz confirmó su asistencia, el cupo de las 02:00 PM del 2025-06-20 es exclusivo."
)

verificar(
    "confirmar una prioridad ya confirmada lo indica sin cambiar nada",
    gym_c.confirmar_prioridad("950", "02:00 PM", "2025-06-20", datetime(2025, 6, 20, 11, 30)),
    "Fabián Ortiz ya había confirmado el cupo de las 02:00 PM del 2025-06-20."
)

# Nueva prioridad para probar el caso de NO confirmar a tiempo.
gym_c.registrar_usuario("Gina Paz", "951", "Sociología")
gym_c.registrar_visita("951", "10:00 AM", 30, ["bicicleta"])
gym_c.registrar_visita("951", "10:00 AM", 30, ["bicicleta"])
gym_c.registrar_visita("951", "10:00 AM", 30, ["bicicleta"])
gym_c.prioridad_membresia("951", "10:00 AM", "2025-06-21", datetime(2025, 6, 21, 6, 0))

verificar(
    "confirmar después del límite de 2 horas libera el cupo",
    gym_c.confirmar_prioridad("951", "10:00 AM", "2025-06-21", datetime(2025, 6, 21, 9, 0)),
    "Gina Paz no confirmó a tiempo, el cupo de las 10:00 AM del 2025-06-21 queda libre."
)

verificar(
    "tras liberarse, ya no queda registrada la prioridad",
    len(gym_c.prioridades),
    1  # solo queda la de Fabián, ya confirmada
)

verificar(
    "otro usuario ya puede tomar prioridad sobre el cupo liberado",
    gym_c.confirmar_prioridad("951", "10:00 AM", "2025-06-21", datetime(2025, 6, 21, 9, 30)),
    "No se encontró una prioridad con esos datos."
)

# ===================================================================
# 15. _liberar_prioridades_vencidas (indirectamente, vía realizar_reserva)
# ===================================================================
print("\n--- liberación automática de prioridades vencidas ---")

gym_v = Gym("Gimnasio Vencidas")
gym_v.registrar_usuario("Hugo Salas", "960", "Arquitectura")
gym_v.registrar_usuario("Irene Toro", "961", "Diseño")
gym_v.registrar_visita("960", "08:00 AM", 20, ["pesas"])
gym_v.registrar_visita("960", "08:00 AM", 20, ["pesas"])
gym_v.registrar_visita("960", "08:00 AM", 20, ["pesas"])

gym_v.prioridad_membresia("960", "08:00 AM", "2025-06-25", datetime(2025, 6, 25, 6, 0))

verificar(
    "antes de vencer, otro usuario no puede reservar el horario",
    gym_v.realizar_reserva("961", "08:00 AM", "2025-06-25", datetime(2025, 6, 25, 6, 0)),
    "El horario 08:00 AM del 2025-06-25 está apartado con prioridad para Hugo Salas."
)

verificar(
    "tras pasar el límite de 2 horas, otro usuario sí puede reservar el horario",
    gym_v.realizar_reserva("961", "08:00 AM", "2025-06-25", datetime(2025, 6, 25, 7, 0)),
    "¡Reserva exitosa! Irene Toro tiene su espacio a las 08:00 AM. "
    "el tiempo para estar haciendo uso del gym es: 1:30 horas."
)

verificar(
    "la prioridad vencida ya no está en la lista",
    len(gym_v.prioridades),
    0
)

# ===================================================================
# RESUMEN FINAL
# ===================================================================
print("\n" + "=" * 50)
print(f"RESULTADO: {pruebas_ok}/{pruebas_totales} pruebas pasaron")
print("=" * 50)
