"""Punto de entrada: arma repositorios, GymService e interfaz.

Uso:
    python main.py            abre la interfaz gráfica
    python main.py --demo     abre la interfaz con datos de ejemplo
    python main.py --consola  corre el flujo de punta a punta en la consola
"""
import argparse
from datetime import datetime, timedelta

from excepciones import GymError
from repositorios import ReservaRepositorioMemoria, UsuarioRepositorioMemoria
from servicios import GymService


def crear_servicio() -> GymService:
    """Crea los repositorios en memoria y el servicio que los usa.

    Cuando se fusionen los otros módulos, pasar aquí también VisitaRepositorioMemoria
    y PrioridadRepositorioMemoria como tercer y cuarto argumento.
    """
    return GymService(UsuarioRepositorioMemoria(), ReservaRepositorioMemoria())


def fecha_de_manana() -> str:
    """Devuelve la fecha de mañana en formato AAAA-MM-DD."""
    return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


def cargar_datos_demo(gym: GymService) -> None:
    """Carga usuarios y una reserva de ejemplo."""
    gym.registrar_usuario("Mariana Restrepo", "1004", "Administración de Empresas")
    gym.registrar_usuario("Diego Vega", "1005", "Ingeniería de Sistemas")
    gym.registrar_usuario("Carla Ríos", "800", "Medicina")
    gym.realizar_reserva("1004", "08:00 AM", fecha_de_manana())


def _intentar(titulo: str, accion, *args) -> None:
    """Ejecuta una acción e imprime su resultado o el error de negocio."""
    try:
        print(f"[OK]    {titulo}: {accion(*args)}")
    except GymError as error:
        print(f"[ERROR] {titulo}: {type(error).__name__} -> {error}")


def flujo_consola(gym: GymService) -> None:
    """Recorre de punta a punta los requisitos R1, R2, R3, R7 y R8."""
    fecha = fecha_de_manana()
    _intentar("Registrar usuario", gym.registrar_usuario, "Mariana Restrepo", "1004", "Administración")
    _intentar("Registrar duplicado", gym.registrar_usuario, "Otra Persona", "1004", "Medicina")
    _intentar("Registrar con nombre vacío", gym.registrar_usuario, "", "55", "Medicina")
    _intentar("Registrar segundo usuario", gym.registrar_usuario, "Diego Vega", "1005", "Sistemas")
    _intentar("Reservar", gym.realizar_reserva, "1004", "08:00 AM", fecha)
    _intentar("Segunda reserva el mismo día", gym.realizar_reserva, "1004", "10:00 AM", fecha)
    _intentar("Horario inválido", gym.realizar_reserva, "1005", "09:00 AM", fecha)
    _intentar("Fecha inválida", gym.realizar_reserva, "1005", "08:00 AM", "2025-02-29")
    _intentar("Cancelar", gym.cancelar_reserva, "1004", "08:00 AM", fecha)
    _intentar("Cancelar de nuevo", gym.cancelar_reserva, "1004", "08:00 AM", fecha)
    _intentar("Confirmar (reactivar)", gym.confirmar_reserva, "1004", "08:00 AM", fecha)
    _intentar("Eliminar con nombre incorrecto", gym.eliminar_usuario, "Nadie", "1004")
    _intentar("Eliminar usuario", gym.eliminar_usuario, "Mariana Restrepo", "1004")
    print(f"Usuarios restantes: {[u.nombre for u in gym.listar_usuarios()]}")
    print(f"Reservas restantes: {len(gym.listar_reservas())}")


def iniciar_interfaz(gym: GymService) -> None:
    """Abre la ventana principal con pestañas."""
    from interfaz.ventana_principal import VentanaPrincipal
    VentanaPrincipal(gym).mainloop()


def main() -> None:
    """Lee los argumentos y arranca la consola o la interfaz."""
    lector = argparse.ArgumentParser(description="Sistema de gestión de gimnasio universitario")
    lector.add_argument("--demo", action="store_true", help="carga datos de ejemplo")
    lector.add_argument("--consola", action="store_true", help="corre el flujo en consola")
    argumentos = lector.parse_args()

    gym = crear_servicio()
    if argumentos.consola:
        flujo_consola(gym)
        return
    if argumentos.demo:
        cargar_datos_demo(gym)
    iniciar_interfaz(gym)


if __name__ == "__main__":
    main()
