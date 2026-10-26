"""Pantalla P5: métricas y gráficos estadísticos (Juan José - HU-06)."""
from tkinter import ttk

from interfaz.componentes import PanelBase


class PanelEstadisticas(PanelBase):
    """Visualización analítica del uso del gimnasio con indicadores y gráficos matplotlib."""

    def __init__(self, master, gym) -> None:
        super().__init__(master, gym)

        # Panel superior de indicadores clave
        marco_kpi = ttk.LabelFrame(self, text="Indicadores Principales")
        marco_kpi.pack(fill="x", padx=10, pady=8)

        self.lbl_horario = ttk.Label(marco_kpi, text="Horario pico: -", font=("Segoe UI", 10, "bold"))
        self.lbl_horario.grid(row=0, column=0, padx=15, pady=6, sticky="w")

        self.lbl_programa = ttk.Label(marco_kpi, text="Carrera frecuente: -", font=("Segoe UI", 10, "bold"))
        self.lbl_programa.grid(row=0, column=1, padx=15, pady=6, sticky="w")

        self.lbl_equipo = ttk.Label(marco_kpi, text="Equipo top: -", font=("Segoe UI", 10, "bold"))
        self.lbl_equipo.grid(row=0, column=2, padx=15, pady=6, sticky="w")

        ttk.Button(marco_kpi, text="Actualizar Métricas", command=self.refrescar).grid(
            row=0, column=3, padx=15, pady=6, sticky="e"
        )

        # Contenedor de gráficos
        self.marco_graficos = ttk.Frame(self)
        self.marco_graficos.pack(fill="both", expand=True, padx=10, pady=8)

        self.canvas = None
        self.refrescar()

    def refrescar(self) -> None:
        """Actualiza los indicadores de texto y redibuja los gráficos."""
        # 1. Indicadores textuales
        self.lbl_horario.config(text=self.gym.horario_mas_frecuente())
        self.lbl_programa.config(text=self.gym.programa_mas_frecuente())
        self.lbl_equipo.config(text=self.gym.equipo_mas_utilizado())

        # 2. Gráficos interactivos con matplotlib
        self._dibujar_graficos()

    def _dibujar_graficos(self) -> None:
        """Genera los gráficos de barras embebidos en Tkinter."""
        # Limpiar gráfico previo
        for widget in self.marco_graficos.winfo_children():
            widget.destroy()

        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            from matplotlib.figure import Figure
        except ImportError:
            ttk.Label(
                self.marco_graficos,
                text="Librería 'matplotlib' no instalada.\nPara ver los gráficos, ejecute: pip install matplotlib",
                justify="center",
                font=("Segoe UI", 11)
            ).pack(expand=True)
            return

        datos_duracion = self.gym.datos_promedio_duracion()
        datos_equipos = self.gym.ranking_equipos()

        if not datos_duracion and not datos_equipos:
            ttk.Label(
                self.marco_graficos,
                text="Sin datos registrados para graficar.\nRegistre visitas y usuarios para visualizar estadísticas.",
                justify="center",
                font=("Segoe UI", 11)
            ).pack(expand=True)
            return

        fig = Figure(figsize=(9, 4.2), dpi=100)
        fig.subplots_adjust(bottom=0.25, wspace=0.35)

        # Gráfico 1: Tiempo promedio por usuario
        ax1 = fig.add_subplot(121)
        if datos_duracion:
            nombres = [item[0].split(" (")[0] for item in datos_duracion[:6]]
            tiempos = [item[1] for item in datos_duracion[:6]]
            barras1 = ax1.bar(nombres, tiempos, color="#3498db", edgecolor="#2980b9")
            ax1.set_title("Duración Promedio (min)", fontsize=10, fontweight="bold")
            ax1.set_ylabel("Minutos")
            ax1.tick_params(axis="x", rotation=25, labelsize=8)
            ax1.bar_label(barras1, fmt="%.1f", padding=3, fontsize=8)
        else:
            ax1.text(0.5, 0.5, "Sin datos de duración", ha="center", va="center")
            ax1.axis("off")

        # Gráfico 2: Ranking de equipos
        ax2 = fig.add_subplot(122)
        if datos_equipos:
            equipos = [item[0] for item in datos_equipos[:6]]
            usos = [item[1] for item in datos_equipos[:6]]
            barras2 = ax2.bar(equipos, usos, color="#2ecc71", edgecolor="#27ae60")
            ax2.set_title("Frecuencia de Uso de Equipos", fontsize=10, fontweight="bold")
            ax2.set_ylabel("Número de visitas")
            ax2.tick_params(axis="x", rotation=25, labelsize=8)
            ax2.bar_label(barras2, fmt="%d", padding=3, fontsize=8)
        else:
            ax2.text(0.5, 0.5, "Sin datos de equipos", ha="center", va="center")
            ax2.axis("off")

        self.canvas = FigureCanvasTkAgg(fig, master=self.marco_graficos)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
