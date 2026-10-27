"""Módulo de notificaciones por correo electrónico (Notificador).

Envía correos de confirmación de reserva desde una cuenta de Gmail
configurada en las variables de entorno (o con credenciales explícitas).

La configuración SMTP se lee de variables de entorno para no exponer
contraseñas en el código fuente:
    GYM_EMAIL_REMITENTE   dirección de Gmail del remitente
    GYM_EMAIL_PASSWORD    contraseña de aplicación de Gmail (App Password)

Si las variables no están configuradas el módulo trabaja en modo silencioso
(solo registra la notificación en la consola/log) sin lanzar excepciones
que interrumpan el flujo principal.
"""
from __future__ import annotations

import os
import re
import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Callable


# Patrón básico de validación de correo electrónico
_PATRON_CORREO = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")

# Servidor SMTP de Gmail (funciona también con Outlook cambiando host y puerto)
_SMTP_HOST = "smtp.gmail.com"
_SMTP_PORT = 587


def correo_valido(correo: str) -> bool:
    """Devuelve True si la cadena tiene el formato mínimo de un correo electrónico."""
    return bool(_PATRON_CORREO.match(correo.strip()))


def _construir_mensaje(
    destinatario: str,
    nombre_usuario: str,
    horario: str,
    fecha: str,
    remitente: str,
) -> MIMEMultipart:
    """Construye el objeto MIME con asunto y cuerpo HTML de la confirmación."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"✅ Reserva confirmada – Gimnasio Universitario ({fecha})"
    msg["From"] = remitente
    msg["To"] = destinatario

    texto_plano = (
        f"Hola {nombre_usuario},\n\n"
        f"Tu reserva en el Gimnasio Universitario de la Universidad de Medellín "
        f"ha sido confirmada exitosamente.\n\n"
        f"  Fecha:   {fecha}\n"
        f"  Horario: {horario}\n\n"
        f"Recuerda que la sesión tiene una duración máxima de 1:30 horas.\n"
        f"Si necesitas cancelar o modificar tu reserva, comunícate con el encargado.\n\n"
        f"Saludos,\nGimnasio Universitario – Universidad de Medellín"
    )

    html = f"""\
<html>
  <body style="font-family:Arial,sans-serif;color:#333;margin:0;padding:0;">
    <table width="100%" style="background:#f4f4f4;padding:30px 0;">
      <tr>
        <td align="center">
          <table width="580" style="background:#fff;border-radius:8px;overflow:hidden;
                 box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <!-- Cabecera roja institucional -->
            <tr>
              <td style="background:#D2232A;padding:20px 30px;">
                <h2 style="margin:0;color:#fff;font-size:20px;">
                  🏋️ Gimnasio Universitario
                </h2>
                <p style="margin:4px 0 0;color:#ffd6d6;font-size:13px;">
                  Universidad de Medellín
                </p>
              </td>
            </tr>
            <!-- Cuerpo -->
            <tr>
              <td style="padding:30px;">
                <p style="font-size:16px;">Hola, <strong>{nombre_usuario}</strong> 👋</p>
                <p>Tu reserva en el <strong>Gimnasio Universitario</strong>
                   ha sido <span style="color:#2e7d32;font-weight:bold;">confirmada</span>
                   exitosamente.</p>
                <table style="width:100%;background:#f9f9f9;border-radius:6px;
                       padding:16px;margin:20px 0;border-left:4px solid #D2232A;">
                  <tr>
                    <td style="padding:6px 0;"><strong>📅 Fecha:</strong></td>
                    <td style="padding:6px 0;">{fecha}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0;"><strong>🕐 Horario:</strong></td>
                    <td style="padding:6px 0;">{horario}</td>
                  </tr>
                  <tr>
                    <td style="padding:6px 0;"><strong>⏱ Duración máx.:</strong></td>
                    <td style="padding:6px 0;">1:30 horas (90 minutos)</td>
                  </tr>
                </table>
                <p style="font-size:13px;color:#555;">
                  Si necesitas cancelar o modificar tu reserva, comunícate
                  directamente con el <em>Encargado de las reservas</em>.
                </p>
                <p style="font-size:13px;color:#555;">
                  Antes de esta solución digital el proceso se gestionaba
                  manualmente en hojas de Excel — ahora todo queda registrado
                  de forma centralizada y recibes este correo de forma automática.
                </p>
              </td>
            </tr>
            <!-- Pie -->
            <tr>
              <td style="background:#f0f0f0;padding:14px 30px;font-size:12px;color:#888;
                         text-align:center;">
                Gimnasio Universitario · Universidad de Medellín<br>
                Este mensaje fue generado automáticamente. No responder.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>"""

    msg.attach(MIMEText(texto_plano, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    return msg


def _enviar_en_hilo(
    destinatario: str,
    nombre_usuario: str,
    horario: str,
    fecha: str,
    remitente: str,
    password: str,
    callback_error: Callable[[str], None] | None = None,
) -> None:
    """Lógica real de envío, ejecutada en un hilo secundario para no bloquear la UI."""
    try:
        msg = _construir_mensaje(destinatario, nombre_usuario, horario, fecha, remitente)
        with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT, timeout=10) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.login(remitente, password)
            servidor.sendmail(remitente, [destinatario], msg.as_string())
        print(f"[Notificador] Correo enviado a {destinatario} ({nombre_usuario}).")
    except smtplib.SMTPAuthenticationError:
        msg_error = (
            "No se pudo autenticar con el servidor de correo. "
            "Verifica GYM_EMAIL_REMITENTE y GYM_EMAIL_PASSWORD."
        )
        print(f"[Notificador] ERROR: {msg_error}")
        if callback_error:
            callback_error(msg_error)
    except Exception as exc:  # noqa: BLE001
        msg_error = f"Error al enviar correo: {exc}"
        print(f"[Notificador] ERROR: {msg_error}")
        if callback_error:
            callback_error(msg_error)


def enviar_confirmacion_reserva(
    destinatario: str,
    nombre_usuario: str,
    horario: str,
    fecha: str,
    callback_error: Callable[[str], None] | None = None,
) -> bool:
    """Envía la notificación de reserva confirmada.

    Obtiene las credenciales de las variables de entorno:
        GYM_EMAIL_REMITENTE   dirección Gmail del gimnasio
        GYM_EMAIL_PASSWORD    contraseña de aplicación de Gmail

    Si las variables no están configuradas imprime una advertencia en consola
    y retorna False (sin lanzar excepción).

    Parámetros
    ----------
    destinatario : str
        Correo electrónico del usuario que realizó la reserva.
    nombre_usuario : str
        Nombre completo del titular.
    horario : str
        Franja horaria de la reserva (p. ej. «08:00 AM»).
    fecha : str
        Fecha de la reserva en formato AAAA-MM-DD.
    callback_error : Callable[[str], None] | None
        Función opcional que se invoca con el mensaje de error si el envío falla.

    Retorna
    -------
    bool
        True si el envío se lanzó en hilo, False si faltan credenciales.
    """
    remitente = os.environ.get("GYM_EMAIL_REMITENTE", "").strip()
    password = os.environ.get("GYM_EMAIL_PASSWORD", "").strip()

    if not remitente or not password:
        print(
            "[Notificador] Credenciales no configuradas. "
            "Define GYM_EMAIL_REMITENTE y GYM_EMAIL_PASSWORD para activar los correos."
        )
        return False

    hilo = threading.Thread(
        target=_enviar_en_hilo,
        args=(destinatario, nombre_usuario, horario, fecha, remitente, password, callback_error),
        daemon=True,
    )
    hilo.start()
    return True
