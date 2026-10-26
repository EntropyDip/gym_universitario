"""Pantalla P4: solicitud y confirmación de prioridades (Angelina - HU-09)."""
from tkinter import messagebox, ttk

from interfaz.componentes import (
    PanelBase,
    SelectorFecha,
    SelectorHorario,
    TablaDatos,
)


class PanelPrioridades(PanelBase):
    """Gestión de cupos prioritarios de membresía por fidelidad y tiempo acumulado."""

    def __init__(self, master, gym) -> None:
        super().__init__(master, gym)

        formulario = ttk.LabelFrame(self, text="Solicitud y Confirmación de Prioridad")
        formulario.pack(fill="x", padx=10, pady=8)

        ttk.Label(formulario, text="Documento:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.entrada_doc = ttk.Entry(formulario, width=18)
        self.entrada_doc.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(formulario, text="Fecha:").grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.selector_fecha = SelectorFecha(formulario)
        self.selector_fecha.grid(row=0, column=3, padx=5, pady=4)

        ttk.Label(formulario, text="Horario:").grid(row=0, column=4, padx=5, pady=4, sticky="w")
        self.selector_horario = SelectorHorario(formulario, gym.horarios_disponibles)
        self.selector_horario.grid(row=0, column=5, padx=5, pady=4)

        botones = ttk.Frame(formulario)
        botones.grid(row=1, column=0, columnspan=6, pady=6)
        ttk.Button(botones, text="Solicitar Prioridad", command=self.solicitar).pack(side="left", padx=5)
        ttk.Button(botones, text="Confirmar Asistencia", command=self.confirmar).pack(side="left", padx=5)

        # Reglas explicativas
        nota = (
            "Nota: Para obtener prioridad debe ser usuario habitual (≥3 visitas en el horario) "
            "o acumular mayor tiempo total que cualquier otro usuario. Debe confirmar su asistencia "
            "hasta 2 horas antes de la sesión."
        )
        ttk.Label(self, text=nota, wraplength=800, foreground="#555555").pack(fill="x", padx=10, pady=4)

        # Tabla de prioridades
        self.tabla = TablaDatos(
            self,
            ["Usuario", "Documento", "Fecha", "Horario", "Límite Confirmación", "Estado"]
        )
        self.tabla.pack(fill="both", expand=True, padx=10, pady=8)
        self.refrescar()

    def _datos(self) -> tuple[str, str, str]:
        """Obtiene documento, horario y fecha de los campos."""
        return (
            self.entrada_doc.get().strip(),
            self.selector_horario.obtener(),
            self.selector_fecha.obtener(),
        )

    def solicitar(self) -> None:
        """Pide al servicio otorgar prioridad de membresía (R12)."""
        doc, horario, fecha = self._datos()
        mensaje = self.ejecutar(self.gym.prioridad_membresia, doc, horario, fecha)
        if mensaje:
            messagebox.showinfo("Prioridades", mensaje)
            self.refrescar()

    def confirmar(self) -> None:
        """Pide al servicio confirmar asistencia antes del límite de 2 horas (R13)."""
        doc, horario, fecha = self._datos()
        mensaje = self.ejecutar(self.gym.confirmar_prioridad, doc, horario, fecha)
        if mensaje:
            messagebox.showinfo("Prioridades", mensaje)
            self.refrescar()

    def refrescar(self) -> None:
        """Actualiza la tabla de prioridades vigentes."""
        filas = []
        for p in self.gym.listar_prioridades_vigentes():
            limite_str = p.limite_confirmacion().strftime("%Y-%m-%d %I:%M %p")
            estado = "Confirmada" if p.confirmada else "Pendiente"
            filas.append((p.nombre, p.documento, p.fecha, p.horario, limite_str, estado))
        self.tabla.cargar(filas)
