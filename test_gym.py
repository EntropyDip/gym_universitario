"""Pruebas unitarias completas para los 15 requisitos del sistema.

Organizado por módulos y responsabilidades de los integrantes:
- TestUsuarios & TestReservas: Samuel Zapata Trujillo (HU-01, HU-02)
- TestVisitasYFechas & TestEstadisticas: Juan José Aguirre Durango (HU-04, HU-05)
- TestConsultasYDisponibilidad & TestPrioridades: Angelina Negrette Diaz (HU-07, HU-08)
"""
from datetime import datetime, timedelta
import unittest

from excepciones import (
    CupoApartadoError,
    DatoVacioError,
    DuracionInvalidaError,
    FechaInvalidaError,
    HorarioInvalidoError,
    PrioridadNoCumpleError,
    PrioridadNoEncontradaError,
    ReservaDuplicadaError,
    ReservaNoEncontradaError,
    UsuarioNoRegistradoError,
    UsuarioYaRegistradoError,
)
from modelos import es_bisiesto, es_fecha_valida
from repositorios import (
    PrioridadRepositorioMemoria,
    ReservaRepositorioMemoria,
    UsuarioRepositorioMemoria,
    VisitaRepositorioMemoria,
)
from servicios import GymService


def crear_gym_prueba() -> GymService:
    """Crea una instancia limpia de GymService con repositorios en memoria."""
    return GymService(
        usuarios=UsuarioRepositorioMemoria(),
        reservas=ReservaRepositorioMemoria(),
        visitas=VisitaRepositorioMemoria(),
        prioridades=PrioridadRepositorioMemoria()
    )


# =========================================================================
# MÓDULO 1: USUARIOS Y RESERVAS (Samuel Zapata Trujillo - R1, R2, R3, R7, R8)
# =========================================================================

class TestUsuarios(unittest.TestCase):
    """Pruebas de HU-01: Registro y eliminación de usuarios (R1, R2)."""

    def setUp(self):
        self.gym = crear_gym_prueba()

    def test_registrar_usuario_exitoso(self):
        msg = self.gym.registrar_usuario("Mariana Restrepo", "1004", "Administración")
        self.assertIn("exitosamente", msg)
        self.assertEqual(len(self.gym.listar_usuarios()), 1)

    def test_documento_duplicado_lanza_error(self):
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(UsuarioYaRegistradoError):
            self.gym.registrar_usuario("Otra Persona", "1004", "Medicina")

    def test_documento_con_espacios_es_limpiado(self):
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(UsuarioYaRegistradoError):
            self.gym.registrar_usuario("Mariana", "  1004  ", "Administración")

    def test_campos_vacios_lanzan_error(self):
        for nombre, doc, prog in [("", "1", "Prog"), ("Ana", "", "Prog"), ("Ana", "1", ""), ("  ", "1", "P")]:
            with self.subTest(nombre=nombre, doc=doc, prog=prog):
                with self.assertRaises(DatoVacioError):
                    self.gym.registrar_usuario(nombre, doc, prog)

    def test_eliminar_usuario_inexistente(self):
        with self.assertRaises(UsuarioNoRegistradoError):
            self.gym.eliminar_usuario("Nadie", "999")

    def test_eliminar_con_nombre_incorrecto(self):
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(UsuarioNoRegistradoError):
            self.gym.eliminar_usuario("Otro Nombre", "1004")

    def test_eliminar_en_cascada_reservas_visitas_prioridades(self):
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        self.gym.registrar_usuario("Carlos", "1005", "Sistemas")

        # Crear datos asociados a Mariana
        self.gym.realizar_reserva("1004", "08:00 AM", "2026-11-10")
        self.gym.registrar_visita("1004", "08:00 AM", 60, ["Mancuernas"])
        self.gym.prioridades.agregar(self.gym.usuarios.buscar("1004"))  # mock de objeto con documento

        # Eliminar Mariana
        self.gym.eliminar_usuario("Mariana", "1004")

        self.assertEqual(len(self.gym.listar_usuarios()), 1)
        self.assertEqual(len(self.gym.listar_reservas()), 0)
        self.assertEqual(len(self.gym.listar_visitas()), 0)


class TestReservas(unittest.TestCase):
    """Pruebas de HU-02: Reservas de cupos (R3, R7, R8)."""

    def setUp(self):
        self.gym = crear_gym_prueba()
        self.gym.registrar_usuario("Mariana Restrepo", "1004", "Administración")
        self.gym.registrar_usuario("Diego Vega", "1005", "Sistemas")
        self.fecha = "2026-11-10"

    def test_reserva_exitosa(self):
        msg = self.gym.realizar_reserva("1004", "08:00 AM", self.fecha)
        self.assertIn("¡Reserva exitosa!", msg)
        self.assertEqual(len(self.gym.listar_reservas()), 1)

    def test_reserva_usuario_no_registrado(self):
        with self.assertRaises(UsuarioNoRegistradoError):
            self.gym.realizar_reserva("9999", "08:00 AM", self.fecha)

    def test_reserva_horario_invalido(self):
        with self.assertRaises(HorarioInvalidoError):
            self.gym.realizar_reserva("1004", "05:00 PM", self.fecha)

    def test_reserva_fecha_invalida(self):
        with self.assertRaises(FechaInvalidaError):
            self.gym.realizar_reserva("1004", "08:00 AM", "2025-02-29")  # 2025 no bisiesto

    def test_doble_reserva_activa_misma_fecha(self):
        self.gym.realizar_reserva("1004", "08:00 AM", self.fecha)
        with self.assertRaises(ReservaDuplicadaError):
            self.gym.realizar_reserva("1004", "10:00 AM", self.fecha)

    def test_cancelar_y_confirmar_reserva(self):
        self.gym.realizar_reserva("1004", "08:00 AM", self.fecha)

        # Cancelar
        msg_cancelar = self.gym.cancelar_reserva("1004", "08:00 AM", self.fecha)
        self.assertIn("cancelada", msg_cancelar)

        # Cancelar de nuevo informa sin error
        msg_re_cancelar = self.gym.cancelar_reserva("1004", "08:00 AM", self.fecha)
        self.assertIn("ya estaba cancelada", msg_re_cancelar)

        # Reactivar
        msg_confirmar = self.gym.confirmar_reserva("1004", "08:00 AM", self.fecha)
        self.assertIn("confirmada nuevamente", msg_confirmar)

        # Reactivar de nuevo informa sin error
        msg_re_confirmar = self.gym.confirmar_reserva("1004", "08:00 AM", self.fecha)
        self.assertIn("ya está activa", msg_re_confirmar)

    def test_cancelar_inexistente(self):
        with self.assertRaises(ReservaNoEncontradaError):
            self.gym.cancelar_reserva("1004", "08:00 AM", "2026-12-01")


# =========================================================================
# MÓDULO 2: VISITAS Y ESTADÍSTICAS (Juan José Aguirre - R4, R5, R6, R11, R15)
# =========================================================================

class TestVisitasYFechas(unittest.TestCase):
    """Pruebas de HU-04: Registro de visitas y validación de calendario (R4)."""

    def setUp(self):
        self.gym = crear_gym_prueba()
        self.gym.registrar_usuario("Mariana", "1004", "Administración")

    def test_algoritmo_bisiestos(self):
        self.assertTrue(es_bisiesto(2024))
        self.assertFalse(es_bisiesto(2025))
        self.assertFalse(es_bisiesto(1900))  # Múltiplo de 100 pero no de 400
        self.assertTrue(es_bisiesto(2000))   # Múltiplo de 400

    def test_validador_fechas(self):
        self.assertTrue(es_fecha_valida("2024-02-29"))
        self.assertFalse(es_fecha_valida("2025-02-29"))
        self.assertFalse(es_fecha_valida("2025-13-01"))
        self.assertFalse(es_fecha_valida("2025/06/15"))
        self.assertFalse(es_fecha_valida("texto"))

    def test_registrar_visita_exitoso(self):
        msg = self.gym.registrar_visita("1004", "08:00 AM", 60, ["Mancuernas", "Cinta"])
        self.assertIn("registrada correctamente", msg)
        self.assertEqual(len(self.gym.listar_visitas()), 1)

    def test_registrar_visita_duracion_invalida(self):
        for dur in [0, -15, True, False, "sesenta"]:
            with self.subTest(duracion=dur):
                with self.assertRaises(DuracionInvalidaError):
                    self.gym.registrar_visita("1004", "08:00 AM", dur, ["Mancuernas"])


class TestEstadisticas(unittest.TestCase):
    """Pruebas de HU-05: Estadísticas y métricas analíticas (R5, R6, R11, R15)."""

    def setUp(self):
        self.gym = crear_gym_prueba()
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        self.gym.registrar_usuario("Diego", "1005", "Sistemas")
        self.gym.registrar_usuario("Carla", "1006", "Sistemas")

    def test_estadisticas_sin_datos(self):
        self.assertIn("No hay visitas registradas", self.gym.horario_mas_frecuente())
        self.assertIn("No hay registros de uso", self.gym.equipo_mas_utilizado())
        self.assertEqual(self.gym.datos_promedio_duracion(), [])

    def test_programa_mas_frecuente(self):
        self.assertIn("Sistemas", self.gym.programa_mas_frecuente())

    def test_metricas_completas_visitas(self):
        self.gym.registrar_visita("1004", "08:00 AM", 40, ["Mancuernas", "Cinta"])
        self.gym.registrar_visita("1004", "08:00 AM", 60, ["Mancuernas"])
        self.gym.registrar_visita("1005", "10:00 AM", 90, ["Cinta"])

        # Horario más frecuente: 08:00 AM (2 visitas)
        self.assertIn("08:00 AM", self.gym.horario_mas_frecuente())

        # Promedio: Mariana tiene 40 + 60 = 100 / 2 = 50.0
        datos = dict(self.gym.datos_promedio_duracion())
        nombre_clave = [k for k in datos if "1004" in k][0]
        self.assertEqual(datos[nombre_clave], 50.0)

        # Ranking de equipos: Mancuernas (2 visitas), Cinta (2 visitas)
        ranking = dict(self.gym.ranking_equipos())
        self.assertEqual(ranking["Mancuernas"], 2)






# =========================================================================
# MÓDULO 3: PRIORIDADES Y CONSULTAS (Angelina Negrette - R9, R10, R12, R13, R14)
# =========================================================================


class TestConsultasYDisponibilidad(unittest.TestCase):
    """Pruebas de HU-07: Verificación de propietario, resumen y disponibilidad (R9, R10, R14)."""

    def setUp(self):
        self.gym = crear_gym_prueba()
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        self.fecha = "2026-11-15"

    def test_verificar_propietario(self):
        self.assertEqual(self.gym.verificar_propietario_reserva("1004"), "No")
        self.gym.realizar_reserva("1004", "08:00 AM", self.fecha)
        self.assertEqual(self.gym.verificar_propietario_reserva("1004"), "Sí")

    def test_mostrar_resumen_reserva(self):
        with self.assertRaises(ReservaNoEncontradaError):
            self.gym.mostrar_resumen_reserva("1004")
        self.gym.realizar_reserva("1004", "08:00 AM", self.fecha)
        resumen = self.gym.mostrar_resumen_reserva("1004")
        self.assertIn("Mariana", resumen)
        self.assertIn("08:00 AM", resumen)

    def test_consultar_disponibilidad(self):
        self.gym.realizar_reserva("1004", "08:00 AM", self.fecha)
        disp = self.gym.consultar_disponibilidad(self.fecha)
        estados = {horario: estado for horario, estado, _ in disp}
        self.assertEqual(estados["08:00 AM"], "reservado")
        self.assertEqual(estados["10:00 AM"], "libre")
        self.assertEqual(estados["02:00 PM"], "libre")


class TestPrioridades(unittest.TestCase):
    """Pruebas de HU-08: Sistema dinámico de prioridades y caducidad (R12, R13)."""

    def setUp(self):
        self.gym = crear_gym_prueba()
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        self.gym.registrar_usuario("Diego", "1005", "Sistemas")
        self.fecha = "2026-11-20"
        self.horario = "08:00 AM"
        # 1 día antes a las 08:00 AM (tiempo de sobra antes de las 2 horas límite)
        self.hora_solicitud = datetime(2026, 11, 19, 8, 0)

    def test_prioridad_por_usuario_habitual(self):
        # Mariana registra 3 visitas a las 08:00 AM
        for _ in range(3):
            self.gym.registrar_visita("1004", self.horario, 45, ["Mancuernas"])

        msg = self.gym.prioridad_membresia("1004", self.horario, self.fecha, self.hora_solicitud)
        self.assertIn("obtuvo prioridad", msg)
        self.assertEqual(len(self.gym.listar_prioridades()), 1)

    def test_prioridad_rechazada_si_no_cumple(self):
        # Solo 1 visita
        self.gym.registrar_visita("1004", self.horario, 45, ["Mancuernas"])
        self.gym.registrar_visita("1005", "10:00 AM", 60, ["Poleas"])

        with self.assertRaises(PrioridadNoCumpleError):
            self.gym.prioridad_membresia("1004", self.horario, self.fecha, self.hora_solicitud)


    def test_cupo_con_prioridad_no_puede_ser_reservado_por_otro(self):
        for _ in range(3):
            self.gym.registrar_visita("1004", self.horario, 45, ["Mancuernas"])
        self.gym.prioridad_membresia("1004", self.horario, self.fecha, self.hora_solicitud)

        # Diego intenta reservar ese cupo
        with self.assertRaises(CupoApartadoError):
            self.gym.realizar_reserva("1005", self.horario, self.fecha, self.hora_solicitud)

    def test_confirmar_prioridad_a_tiempo(self):
        for _ in range(3):
            self.gym.registrar_visita("1004", self.horario, 45, ["Mancuernas"])
        self.gym.prioridad_membresia("1004", self.horario, self.fecha, self.hora_solicitud)

        # Confirmar 3 horas antes del horario (05:00 AM del mismo día) -> Límite es 06:00 AM
        hora_confirmacion = datetime(2026, 11, 20, 5, 0)
        msg = self.gym.confirmar_prioridad("1004", self.horario, self.fecha, hora_confirmacion)
        self.assertIn("confirmó su asistencia", msg)
        self.assertTrue(self.gym.listar_prioridades()[0].confirmada)

    def test_confirmar_prioridad_tarde_libera_cupo(self):
        for _ in range(3):
            self.gym.registrar_visita("1004", self.horario, 45, ["Mancuernas"])
        self.gym.prioridad_membresia("1004", self.horario, self.fecha, self.hora_solicitud)

        # Confirmar 1 hora antes (07:00 AM) -> Ya venció el límite de 2 horas (06:00 AM)
        hora_tardia = datetime(2026, 11, 20, 7, 0)
        msg = self.gym.confirmar_prioridad("1004", self.horario, self.fecha, hora_tardia)
        self.assertIn("queda libre", msg)
        self.assertEqual(len(self.gym.listar_prioridades()), 0)


if __name__ == "__main__":
    unittest.main()





