"""Pruebas unitarias. Cada integrante escribe la clase de su módulo."""
import unittest
from datetime import datetime
from types import SimpleNamespace

from excepciones import (DatoVacioError, UsuarioNoRegistradoError, UsuarioYaRegistradoError, CupoApartadoError, FechaInvalidaError, GymError,
        HorarioInvalidoError, ReservaDuplicadaError, ReservaNoEncontradaError)
from repositorios import UsuarioRepositorioMemoria
from servicios import GymService

AHORA = datetime(2025, 6, 1, 8, 0)
FECHA = "2025-06-15"

class RepoFalso:
    """Repositorio de prueba que guarda objetos y soporta eliminar_por_documento."""

    def __init__(self, elementos=None):
        self.elementos = list(elementos or [])

    def listar(self):
        return list(self.elementos)

    def eliminar_por_documento(self, documento):
        self.elementos = [e for e in self.elementos if e.documento != documento]


def crear_gym(reservas=None, visitas=None, prioridades=None):
    """Crea un GymService de prueba (en HU-02 se reemplaza por la versión con ReservaRepositorioMemoria)."""
    return GymService(UsuarioRepositorioMemoria(), reservas or RepoFalso(), visitas, prioridades)


class TestUsuarios(unittest.TestCase):
    """Pruebas de HU-01 (Samuel): R1 y R2."""

    def setUp(self):
        self.gym = crear_gym()

    def test_registrar_usuario_exitoso(self):
        mensaje = self.gym.registrar_usuario("Mariana Restrepo", "1004", "Administración")
        self.assertEqual(mensaje, "Usuario Mariana Restrepo registrado exitosamente.")
        self.assertEqual(len(self.gym.listar_usuarios()), 1)

    def test_documento_duplicado_no_modifica_nada(self):
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(UsuarioYaRegistradoError):
            self.gym.registrar_usuario("Otra Persona", "1004", "Medicina")
        usuarios = self.gym.listar_usuarios()
        self.assertEqual(len(usuarios), 1)
        self.assertEqual(usuarios[0].nombre, "Mariana")

    def test_documento_con_espacios_cuenta_como_el_mismo(self):
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(UsuarioYaRegistradoError):
            self.gym.registrar_usuario("Mariana", "1004  ", "Administración")

    def test_datos_vacios(self):
        for datos in (("", "1", "Prog"), ("Ana", "", "Prog"), ("Ana", "1", ""),
                      ("   ", "1", "Prog")):
            with self.subTest(datos=datos):
                with self.assertRaises(DatoVacioError):
                    self.gym.registrar_usuario(*datos)
        self.assertEqual(self.gym.listar_usuarios(), [])

    def test_eliminar_con_nombre_que_no_coincide(self):
        self.gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(UsuarioNoRegistradoError):
            self.gym.eliminar_usuario("Otro Nombre", "1004")
        self.assertEqual(len(self.gym.listar_usuarios()), 1)

    def test_eliminar_documento_inexistente(self):
        with self.assertRaises(UsuarioNoRegistradoError):
            self.gym.eliminar_usuario("Mariana", "999")

    def test_eliminar_en_cascada(self):
        reserva = SimpleNamespace(documento="1004")
        otra_reserva = SimpleNamespace(documento="2")
        visita = SimpleNamespace(documento="1004")
        otra_visita = SimpleNamespace(documento="2")
        prioridad = SimpleNamespace(documento="1004")
        reservas, visitas, prioridades = (RepoFalso([reserva, otra_reserva]),
                                          RepoFalso([visita, otra_visita]),
                                          RepoFalso([prioridad]))
        gym = crear_gym(reservas, visitas, prioridades)
        gym.registrar_usuario("Mariana", "1004", "Administración")
        gym.registrar_usuario("Luis", "2", "Medicina")

        mensaje = gym.eliminar_usuario("Mariana", "1004")

        self.assertEqual(mensaje, "El usuario identificado con 1004 se eliminó correctamente.")
        self.assertEqual([u.documento for u in gym.listar_usuarios()], ["2"])
        self.assertEqual(reservas.listar(), [otra_reserva])
        self.assertEqual(visitas.listar(), [otra_visita])
        self.assertEqual(prioridades.listar(), [])


if __name__ == "__main__":
    unittest.main()
