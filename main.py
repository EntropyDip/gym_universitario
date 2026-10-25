"""Punto de entrada: arma repositorios, GymService e interfaz.

Uso:
    python main.py            abre la interfaz gráfica
    python main.py --demo     abre la interfaz con datos de ejemplo
    python main.py --consola  corre el flujo completo de los 15 requisitos en la consola
"""
import argparse
from datetime import datetime, timedelta

from excepciones import GymError
from repositorios import (
    PrioridadRepositorioMemoria,
    ReservaRepositorioMemoria,
    UsuarioRepositorioMemoria,
    VisitaRepositorioMemoria,
)
from servicios import GymService


def crear_servicio() -> GymService:
    """Instancia los repositorios en memoria y el servicio principal con inyección de dependencias."""
    return GymService(
        usuarios=UsuarioRepositorioMemoria(),
        reservas=ReservaRepositorioMemoria(),
        visitas=VisitaRepositorioMemoria(),
        prioridades=PrioridadRepositorioMemoria()
    )


def fecha_de_manana() -> str:
    """Devuelve la fecha de mañana en formato AAAA-MM-DD."""
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def cargar_datos_demo(gym: GymService) -> None:
    """Carga un conjunto representativo de datos de ejemplo en todos los módulos."""
    # 1. Usuarios (R1)
    gym.registrar_usuario("Mariana Restrepo", "1004", "Administración de Empresas")
    gym.registrar_usuario("Diego Vega", "1005", "Ingeniería de Sistemas")
    gym.registrar_usuario("Carla Ríos", "800", "Medicina")
    gym.registrar_usuario("Andrés Morales", "901", "Ingeniería de Sistemas")

    manana = fecha_de_manana()

    # 2. Visitas históricas para estadísticas y fidelidad (R4, R5, R6, R11, R15)
    gym.registrar_visita("1004", "08:00 AM", 60, ["Cinta de correr", "Mancuernas"])
    gym.registrar_visita("1004", "08:00 AM", 75, ["Cinta de correr", "Bicicleta estática"])
    gym.registrar_visita("1004", "08:00 AM", 50, ["Mancuernas", "Banco plano"])  # Habitual a las 08:00 AM

    gym.registrar_visita("1005", "10:00 AM", 90, ["Prensa de piernas", "Poleas"])
    gym.registrar_visita("1005", "02:00 PM", 85, ["Banco plano", "Mancuernas"])

    gym.registrar_visita("800", "08:00 AM", 40, ["Cinta de correr"])

    # 3. Reservas (R3)
    gym.realizar_reserva("1005", "10:00 AM", manana)

    # 4. Prioridad (R12)
    # Mariana cumple condición de habitual en 08:00 AM
    gym.prioridad_membresia("1004", "08:00 AM", manana, datetime.now())


def _intentar(titulo: str, accion, *args) -> None:
    """Ejecuta una acción e imprime su resultado o el error de negocio controlado."""
    try:
        resultado = accion(*args)
        print(f"[OK]    {titulo}: {resultado}")
    except GymError as error:
        print(f"[ERROR] {titulo}: {type(error).__name__} -> {error}")


def flujo_consola(gym: GymService) -> None:
    """Recorre de punta a punta los 15 requisitos funcionales (R1 a R15)."""
    print("\n" + "=" * 70)
    print("EJECUCIÓN DEL FLUJO COMPLETO EN CONSOLA (R1 A R15)")
    print("=" * 70 + "\n")

    fecha = fecha_de_manana()
    ahora = datetime.now()

    # --- MÓDULO 1: USUARIOS Y RESERVAS (Samuel Zapata) ---
    print("--- 1. Gestión de Usuarios y Reservas (Samuel) ---")
    _intentar("R1: Registrar usuario", gym.registrar_usuario, "Mariana Restrepo", "1004", "Administración")
    _intentar("R1: Registrar segundo usuario", gym.registrar_usuario, "Diego Vega", "1005", "Ingeniería de Sistemas")
    _intentar("R1: Registrar duplicado (debe fallar)", gym.registrar_usuario, "Mariana Clon", "1004", "Medicina")
    _intentar("R1: Registrar con campo vacío (debe fallar)", gym.registrar_usuario, "", "1006", "Derecho")

    _intentar("R3: Realizar reserva", gym.realizar_reserva, "1004", "08:00 AM", fecha, ahora)
    _intentar("R3: Segunda reserva mismo día (debe fallar)", gym.realizar_reserva, "1004", "10:00 AM", fecha, ahora)
    _intentar("R3: Horario inválido (debe fallar)", gym.realizar_reserva, "1005", "11:00 AM", fecha, ahora)
    _intentar("R3: Fecha bisiesta inválida (debe fallar)", gym.realizar_reserva, "1005", "08:00 AM", "2025-02-29", ahora)

    _intentar("R7: Cancelar reserva", gym.cancelar_reserva, "1004", "08:00 AM", fecha)
    _intentar("R7: Cancelar reserva ya cancelada", gym.cancelar_reserva, "1004", "08:00 AM", fecha)

    _intentar("R8: Confirmar (reactivar) reserva", gym.confirmar_reserva, "1004", "08:00 AM", fecha, ahora)

    # --- MÓDULO 2: VISITAS Y ESTADÍSTICAS (Juan José Aguirre) ---






    # --- MÓDULO 3: PRIORIDADES Y CONSULTAS (Angelina Negrette) ---

    print("\n--- 3. Prioridades y Consultas de Disponibilidad (Angelina) ---")
    _intentar("R9: Verificar propietario de reserva", gym.verificar_propietario_reserva, "1004")
    _intentar("R9: Verificar propietario inexistente", gym.verificar_propietario_reserva, "9999")
    _intentar("R10: Mostrar resumen de reserva", gym.mostrar_resumen_reserva, "1004")

    # Solicitar prioridad para otra fecha (Mariana es habitual en 08:00 AM con 3 visitas)
    fecha_futura = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    _intentar("R12: Solicitar prioridad de membresía", gym.prioridad_membresia, "1004", "08:00 AM", fecha_futura, ahora)
    _intentar("R12: Solicitar prioridad sin cumplir (debe fallar)", gym.prioridad_membresia, "1005", "02:00 PM", fecha_futura, ahora)

    # Intentar reservar cupo apartado con prioridad por otro
    _intentar("R3: Reservar cupo apartado con prioridad (debe fallar)", gym.realizar_reserva, "1005", "08:00 AM", fecha_futura, ahora)

    # Confirmar prioridad dentro del tiempo límite
    _intentar("R13: Confirmar prioridad de asistencia", gym.confirmar_prioridad, "1004", "08:00 AM", fecha_futura, ahora)

    # R14: Disponibilidad general
    print("\nR14: Consulta de disponibilidad para fecha futura:")
    for horario, estado, detalle in gym.consultar_disponibilidad(fecha_futura, ahora):
        print(f"  - [{horario}] {estado.upper()}: {detalle}")

    # Eliminación en cascada (R2)
    print("\n--- 4. Eliminación en Cascada (Samuel) ---")
    _intentar("R2: Eliminar usuario Diego", gym.eliminar_usuario, "Diego Vega", "1005")
    print(f"Usuarios restantes: {[u.nombre for u in gym.listar_usuarios()]}")
    print(f"Reservas restantes: {len(gym.listar_reservas())}")
    print(f"Visitas restantes: {len(gym.listar_visitas())}")

    print("\n" + "=" * 70)
    print("FIN DEL FLUJO DE PRUEBAS DE CONSOLA")
    print("=" * 70 + "\n")

