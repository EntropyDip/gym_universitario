"""Módulo de notificaciones para confirmaciones de reservas."""
from __future__ import annotations

import re
from collections.abc import Callable

_PATRON_CORREO = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def correo_valido(correo: str) -> bool:
    """Comprueba el formato mínimo de una dirección de correo.

    Parámetros:
        correo: dirección que se desea comprobar.

    Retorna:
        True si tiene una forma básica de correo, False en caso contrario.
    """
    return bool(_PATRON_CORREO.match(correo.strip()))


class NotificadorReservas:
    """Envía confirmaciones por correo con fallback por SMS/WhatsApp.

    Los adaptadores pueden inyectarse como funciones que reciben el destinatario
    y el mensaje; deben retornar True al enviar y False cuando el envío no ocurre.
    El modo predeterminado simula ambos canales y registra el resultado en consola.
    """

    def __init__(
        self,
        enviar_correo: Callable[[str, str], bool] | None = None,
        enviar_sms: Callable[[str, str], bool] | None = None,
    ) -> None:
        """Crea el gestor con proveedores opcionales o simuladores de consola.

        Parámetros:
            enviar_correo: adaptador de correo, con destinatario y texto.
            enviar_sms: adaptador de SMS/WhatsApp, con número y texto.

        Retorna:
            None.
        """
        self._enviar_correo = enviar_correo or self._simular_correo
        self._enviar_sms = enviar_sms or self._simular_sms

    def notificar_reserva(
        self,
        destinatario: str,
        celular: str,
        nombre_usuario: str,
        horario: str,
        fecha: str,
    ) -> bool:
        """Envía la confirmación por correo e intenta SMS/WhatsApp ante un fallo.

        Parámetros:
            destinatario: correo guardado del usuario; puede estar vacío.
            celular: número de celular guardado; puede estar vacío.
            nombre_usuario: titular de la reserva.
            horario: franja confirmada.
            fecha: fecha confirmada.

        Retorna:
            True si el canal principal o el fallback reportó éxito.

        Excepciones:
            No propaga excepciones de los proveedores: las captura, las registra
            y activa el fallback; False indica que no se entregó por ningún canal.
        """
        mensaje = (
            f"Hola {nombre_usuario}, tu reserva en el gimnasio quedó confirmada "
            f"para el {fecha} a las {horario}."
        )
        if destinatario:
            try:
                if self._enviar_correo(destinatario, mensaje):
                    return True
                print("[Notificador] El proveedor de correo informó que no envió el mensaje.")
            except Exception as error:
                print(f"[Notificador] Falló el correo: {type(error).__name__}: {error}")
        else:
            print("[Notificador] No hay correo registrado; se activa el canal alternativo.")

        if not celular:
            print("[Notificador] No hay celular registrado para el fallback SMS/WhatsApp.")
            return False
        try:
            if self._enviar_sms(celular, mensaje):
                return True
            print("[Notificador] El proveedor SMS/WhatsApp informó que no envió el mensaje.")
        except Exception as error:
            print(f"[Notificador] Falló SMS/WhatsApp: {type(error).__name__}: {error}")
        return False

    @staticmethod
    def _simular_correo(destinatario: str, mensaje: str) -> bool:
        """Registra como exitoso el envío de correo en modo de simulación.

        Parámetros:
            destinatario: dirección destino.
            mensaje: confirmación que se simula enviar.

        Retorna:
            True, indicando éxito simulado.

        Excepciones:
            No realiza llamadas externas ni genera errores de proveedor.
        """
        # TODO(API correo): sustituir la simulación de la línea 111 por el SDK e inyectar aquí su token/credencial de API.
        print(f"[Notificador] Correo SIMULADO enviado a {destinatario}: {mensaje}")
        return True

    @staticmethod
    def _simular_sms(celular: str, mensaje: str) -> bool:
        """Registra como exitoso el envío SMS/WhatsApp en modo de simulación.

        Parámetros:
            celular: número de destino.
            mensaje: confirmación que se simula enviar.

        Retorna:
            True, indicando éxito simulado.

        Excepciones:
            No realiza llamadas externas ni genera errores de proveedor.
        """
        # TODO(API SMS/WhatsApp): sustituir la simulación de la línea 129 por el SDK e inyectar aquí su token de API.
        print(f"[Notificador] SMS/WhatsApp SIMULADO enviado a {celular}: {mensaje}")
        return True
