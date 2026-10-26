"""Pantalla P3: registro y control de visitas (Juan José - HU-06)[cite: 11]."""
import tkinter as tk
from tkinter import messagebox, ttk

from interfaz.componentes import PanelBase, SelectorFecha, SelectorHorario, TablaDatos


class PanelVisitas(PanelBase):
    """Formulario para registrar asistencias y tabla de visitas del gimnasio[cite: 11]."""

    EQUIPOS_COMUNES = [
        "Mancuernas",
        "Cinta de correr",
        "Bicicleta estática",
        "Banco plano",
        "Prensa de piernas",
        "Poleas"
    ]

    def __init__(self, master, gym) -> None:
        super().__init__(master, gym)

        formulario = ttk.LabelFrame(self, text="Registro de Visita")
        formulario.pack(fill="x", padx=10, pady=8)

        # Fila 0: Documento, Horario, Duración, Fecha
        ttk.Label(formulario, text="Documento:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.entrada_doc = ttk.Entry(formulario, width=14)
        self.entrada_doc.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(formulario, text="Horario:").grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.selector_horario = SelectorHorario(formulario, gym.horarios_disponibles)
        self.selector_horario.grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(formulario, text="Duración (min):").grid(row=0, column=4, padx=5, pady=4, sticky="w")
        self.entrada_duracion = ttk.Entry(formulario, width=8)
        self.entrada_duracion.grid(row=0, column=5, padx=5, pady=4)

        ttk.Label(formulario, text="Fecha:").grid(row=0, column=6, padx=5, pady=4, sticky="w")
        self.selector_fecha = SelectorFecha(formulario, dias_inicial=0)  # por defecto, hoy[cite: 11]
        self.selector_fecha.grid(row=0, column=7, padx=5, pady=4)

        # Fila 1: Equipos utilizados
        ttk.Label(formulario, text="Equipos comunes:").grid(row=1, column=0, padx=5, pady=4, sticky="nw")
        marco_equipos = ttk.Frame(formulario)
        marco_equipos.grid(row=1, column=1, columnspan=5, sticky="w", pady=4)

        self.check_vars = {}
        for idx, equipo in enumerate(self.EQUIPOS_COMUNES):
            var = tk.BooleanVar(value=False)
            self.check_vars[equipo] = var
            ttk.Checkbutton(marco_equipos, text=equipo, variable=var).grid(
                row=idx // 3, column=idx % 3, padx=4, pady=2, sticky="w"
            )

        ttk.Label(formulario, text="Otros equipos (separados por coma):").grid(
            row=2, column=0, columnspan=2, padx=5, pady=4, sticky="w"
        )
        self.entrada_otros = ttk.Entry(formulario, width=45)
        self.entrada_otros.grid(row=2, column=2, columnspan=4, padx=5, pady=4, sticky="w")

        # Botón de registro
        botones = ttk.Frame(formulario)
        botones.grid(row=3, column=0, columnspan=8, pady=6)
        ttk.Button(botones, text="Registrar Visita", command=self.registrar).pack(side="left", padx=5)

        # Tabla de visitas
        self.tabla = TablaDatos(self, ["Documento", "Fecha", "Horario", "Duración (min)", "Equipos Usados"])
        self.tabla.pack(fill="both", expand=True, padx=10, pady=8)
        self.refrescar()

    def _obtener_equipos(self) -> list[str]:
        """Reúne los equipos seleccionados en checkboxes y los ingresados a mano[cite: 11]."""
        seleccionados = [eq for eq, var in self.check_vars.items() if var.get()]
        otros = self.entrada_otros.get().strip()
        if otros:
            for extra in otros.split(","):
                extra_limpio = extra.strip()
                if extra_limpio and extra_limpio not in seleccionados:
                    seleccionados.append(extra_limpio)
        return seleccionados

    def _limpiar(self) -> None:
        """Limpia los campos del formulario[cite: 11]."""
        self.entrada_doc.delete(0, "end")
        self.entrada_duracion.delete(0, "end")
        self.entrada_otros.delete(0, "end")
        for var in self.check_vars.values():
            var.set(False)

    def registrar(self) -> None:
        """Pide al servicio registrar la visita[cite: 11]."""
        doc = self.entrada_doc.get().strip()
        horario = self.selector_horario.obtener()
        fecha = self.selector_fecha.obtener()
        duracion_texto = self.entrada_duracion.get().strip()

        if not duracion_texto.isdecimal():
            messagebox.showerror("Error", "La duración debe ser un número entero positivo de minutos.")
            return

        duracion = int(duracion_texto)
        equipos = self._obtener_equipos()

        mensaje = self.ejecutar(self.gym.registrar_visita, doc, horario, duracion, equipos, fecha)
        if mensaje:
            messagebox.showinfo("Visitas", mensaje)
            self._limpiar()
            self.refrescar()

    def refrescar(self) -> None:
        """Recarga la tabla de visitas registradas[cite: 11]."""
        filas = [
            (v.documento, v.fecha, v.horario, f"{v.duracion} min", ", ".join(v.equipos) if v.equipos else "Ninguno")
            for v in self.gym.listar_visitas()
        ]
        self.tabla.cargar(filas)
