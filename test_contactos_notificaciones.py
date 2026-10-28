"""Pruebas de persistencia JSON y entrega con canal alternativo."""
import json
from pathlib import Path
import tempfile
import unittest

from excepciones import DatosContactoRequeridosError, PersistenciaError
from modelos import ContactoUsuario
from notificador import NotificadorReservas
from repositorios import (
    ContactoUsuarioRepositorioJSON,
    PrioridadRepositorioMemoria,
    ReservaRepositorioMemoria,
    UsuarioRepositorioMemoria,
    VisitaRepositorioMemoria,
)
from servicios import GymService


class TestContactosJSON(unittest.TestCase):
    """Valida la persistencia mínima de datos y su integración con reservas."""

    def setUp(self) -> None:
        self.directorio = tempfile.TemporaryDirectory()
        self.archivo = Path(self.directorio.name) / "usuarios.json"
        self.contactos = ContactoUsuarioRepositorioJSON(self.archivo)
        self.notificaciones: list[tuple[str, str]] = []
        self.gym = GymService(
            usuarios=UsuarioRepositorioMemoria(),
            reservas=ReservaRepositorioMemoria(),
            visitas=VisitaRepositorioMemoria(),
            prioridades=PrioridadRepositorioMemoria(),
            contactos=self.contactos,
            notificador=NotificadorReservas(
                enviar_correo=lambda destino, _mensaje: (
                    self.notificaciones.append((destino, "correo")) or True
                ),
                enviar_sms=lambda _destino, _mensaje: True,
            ),
        )
        self.gym.registrar_usuario("Ana Torres", "2001", "Medicina")

    def tearDown(self) -> None:
        self.directorio.cleanup()

    def test_solicita_contacto_nuevo_y_guarda_solo_campos_permitidos(self) -> None:
        with self.assertRaises(DatosContactoRequeridosError):
            self.gym.realizar_reserva("2001", "08:00 AM", "2026-11-10")
        self.assertEqual(self.gym.listar_reservas(), [])

        self.gym.realizar_reserva(
            "2001", "08:00 AM", "2026-11-10",
            correo="ana@udem.edu.co", celular="+573001234567",
        )

        registro = json.loads(self.archivo.read_text(encoding="utf-8"))[0]
        self.assertEqual(set(registro), {"identificador", "correo", "celular"})
        self.assertEqual(registro, {
            "identificador": "2001",
            "correo": "ana@udem.edu.co",
            "celular": "+573001234567",
        })

    def test_reutiliza_contacto_guardado_sin_pedirlo_de_nuevo(self) -> None:
        self.contactos.guardar(
            ContactoUsuario("2001", "ana@udem.edu.co", "+573001234567")
        )
        resultado = self.gym.realizar_reserva("2001", "08:00 AM", "2026-11-10")
        self.assertIn("¡Reserva exitosa!", resultado)
        self.assertEqual(self.contactos.buscar("2001").celular, "+573001234567")
        self.assertEqual(self.notificaciones, [("ana@udem.edu.co", "correo")])

    def test_json_corrupto_se_reporta_como_error_de_persistencia(self) -> None:
        self.archivo.write_text("{", encoding="utf-8")
        with self.assertRaises(PersistenciaError):
            self.contactos.listar()

    def test_error_de_escritura_se_reporta_sin_ignorarla(self) -> None:
        destino_es_directorio = Path(self.directorio.name) / "destino"
        destino_es_directorio.mkdir()
        repositorio = ContactoUsuarioRepositorioJSON(destino_es_directorio)
        with self.assertRaises(PersistenciaError):
            repositorio.guardar(
                ContactoUsuario("2001", "ana@udem.edu.co", "+573001234567")
            )

    def test_eliminar_usuario_elimina_su_contacto(self) -> None:
        self.contactos.guardar(
            ContactoUsuario("2001", "ana@udem.edu.co", "+573001234567")
        )
        self.gym.eliminar_usuario("Ana Torres", "2001")
        self.assertIsNone(self.contactos.buscar("2001"))


class TestNotificadorReservas(unittest.TestCase):
    """Comprueba correo principal y fallback de SMS/WhatsApp."""

    def test_excepcion_de_correo_activa_sms(self) -> None:
        destinos_sms: list[str] = []

        def correo_fallido(_destinatario: str, _mensaje: str) -> bool:
            raise RuntimeError("proveedor no disponible")

        notificador = NotificadorReservas(
            enviar_correo=correo_fallido,
            enviar_sms=lambda celular, _mensaje: destinos_sms.append(celular) or True,
        )
        enviado = notificador.notificar_reserva(
            "ana@udem.edu.co", "+573001234567", "Ana", "08:00 AM", "2026-11-10"
        )

        self.assertTrue(enviado)
        self.assertEqual(destinos_sms, ["+573001234567"])

    def test_correo_exitoso_no_usa_sms(self) -> None:
        destinos_sms: list[str] = []
        notificador = NotificadorReservas(
            enviar_correo=lambda _destinatario, _mensaje: True,
            enviar_sms=lambda celular, _mensaje: destinos_sms.append(celular) or True,
        )
        enviado = notificador.notificar_reserva(
            "ana@udem.edu.co", "+573001234567", "Ana", "08:00 AM", "2026-11-10"
        )
        self.assertTrue(enviado)
        self.assertEqual(destinos_sms, [])


if __name__ == "__main__":
    unittest.main()
