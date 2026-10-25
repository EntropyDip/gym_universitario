"""Ventana principal con pestañas para todos los paneles del sistema (Angelina - HU-09)."""
import tkinter as tk
from tkinter import ttk

from interfaz.panel_estadisticas import PanelEstadisticas
from interfaz.panel_prioridades import PanelPrioridades
from interfaz.panel_reservas import PanelReservas
from interfaz.panel_usuarios import PanelUsuarios
from interfaz.panel_visitas import PanelVisitas


class VentanaPrincipal(tk.Tk):
    """Ventana principal contenedora que organiza la navegación mediante pestañas."""

    def __init__(self, gym) -> None:
        super().__init__()
        self.gym = gym

        self.title("Sistema de Gestión de Gimnasio Universitario")
        self.geometry("980x680")
        self.minsize(860, 560)

        # Configurar estilos ttk
        self._configurar_estilos()

        # Cabecera superior
        cabecera = ttk.Frame(self, padding=(15, 10))
        cabecera.pack(fill="x")
        ttk.Label(
            cabecera,
            text=f"🏋️ {self.gym.nombre.upper()}",
            font=("Segoe UI", 16, "bold"),
            foreground="#2c3e50"
        ).pack(side="left")

        subtitulo = f"Sesión máxima: {self.gym.duracion_maxima_sesion} | Horarios: {' · '.join(self.gym.horarios_disponibles)}"
        ttk.Label(
            cabecera,
            text=subtitulo,
            font=("Segoe UI", 9),
            foreground="#7f8c8d"
        ).pack(side="right")

        # Separador visual
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10, pady=(0, 5))

        # Cuaderno de pestañas (Notebook)
        self.cuaderno = ttk.Notebook(self)
        self.cuaderno.pack(fill="both", expand=True, padx=10, pady=5)

        # Instanciar paneles
        self.panel_usuarios = PanelUsuarios(self.cuaderno, self.gym)
        self.panel_reservas = PanelReservas(self.cuaderno, self.gym)
        self.panel_visitas = PanelVisitas(self.cuaderno, self.gym)
        self.panel_prioridades = PanelPrioridades(self.cuaderno, self.gym)
        self.panel_estadisticas = PanelEstadisticas(self.cuaderno, self.gym)

        # Agregar pestañas
        self.cuaderno.add(self.panel_usuarios, text=" 👤 Usuarios ")
        self.cuaderno.add(self.panel_reservas, text=" 📅 Reservas ")
        self.cuaderno.add(self.panel_visitas, text=" ⏱️ Visitas ")
        self.cuaderno.add(self.panel_prioridades, text=" ⭐ Prioridades ")
        self.cuaderno.add(self.panel_estadisticas, text=" 📊 Estadísticas ")

        # Evento para refrescar el panel activo al cambiar de pestaña
        self.cuaderno.bind("<<NotebookTabChanged>>", self._al_cambiar_pestana)

    def _configurar_estilos(self) -> None:
        """Aplica un tema moderno a los widgets ttk."""
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        estilo.configure("TButton", font=("Segoe UI", 9), padding=5)
        estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        estilo.configure("Treeview", font=("Segoe UI", 9), rowheight=24)

    def _al_cambiar_pestana(self, evento) -> None:
        """Llama al método refrescar() del panel que acaba de seleccionarse."""
        id_seleccionado = self.cuaderno.select()
        widget_activo = self.nametowidget(id_seleccionado)
        if hasattr(widget_activo, "refrescar"):
            widget_activo.refrescar()
