"""Pantalla P2: reservas y disponibilidad (R3, R7, R8, R9, R10, R14)."""
from tkinter import messagebox, ttk

from interfaz.componentes import PanelBase, SelectorFecha, SelectorHorario, TablaDatos

COLORES_ESTADO = {"libre": "#d9f2d9", "reservado": "#fff2cc", "apartado": "#f8d7da"}


class PanelReservas(PanelBase):
    """Reservar, cancelar y confirmar; consultar propietario, resumen y disponibilidad."""

    def __init__(self, master, gym):
        super().__init__(master, gym)
        formulario = ttk.LabelFrame(self, text="Reserva")
        formulario.pack(fill="x", padx=10, pady=8)

        ttk.Label(formulario, text="Documento").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.documento = ttk.Entry(formulario, width=20)
        self.documento.grid(row=0, column=1, padx=5, pady=4)
        ttk.Label(formulario, text="Fecha").grid(row=0, column=2, padx=5, sticky="w")
        self.fecha = SelectorFecha(formulario)
        self.fecha.grid(row=0, column=3, padx=5)
        ttk.Label(formulario, text="Horario").grid(row=0, column=4, padx=5, sticky="w")
        self.horario = SelectorHorario(formulario, gym.horarios_disponibles)
        self.horario.grid(row=0, column=5, padx=5)

        botones = ttk.Frame(formulario)
        botones.grid(row=1, column=0, columnspan=6, pady=6)
        for texto, comando in (("Reservar", self.reservar), ("Cancelar", self.cancelar),
                               ("Confirmar", self.confirmar),
                               ("¿Es del usuario?", self.verificar_propietario),
                               ("Ver resumen", self.mostrar_resumen),
                               ("Disponibilidad", self.consultar_disponibilidad)):
            ttk.Button(botones, text=texto, command=comando).pack(side="left", padx=4)

        self.resumen = ttk.Label(self, text="", wraplength=800)
        self.resumen.pack(fill="x", padx=10)

        self.tabla_disponibilidad = TablaDatos(self, ["Horario", "Estado", "Detalle"], alto=3)
        self.tabla_disponibilidad.colorear(COLORES_ESTADO)
        self.tabla_disponibilidad.pack(fill="x", padx=10, pady=6)

        self.tabla_reservas = TablaDatos(self, ["Usuario", "Documento", "Fecha", "Horario", "Estado"])
        self.tabla_reservas.pack(fill="both", expand=True, padx=10, pady=6)
        self.refrescar()

    def _datos(self) -> tuple[str, str, str]:
        """Lee documento, horario y fecha del formulario."""
        return self.documento.get(), self.horario.obtener(), self.fecha.obtener()

    def _accion(self, metodo) -> None:
        """Ejecuta una acción de reserva, muestra el mensaje y actualiza las tablas."""
        mensaje = self.ejecutar(metodo, *self._datos())
        if mensaje:
            messagebox.showinfo("Reservas", mensaje)
            self.refrescar()
            self.consultar_disponibilidad()

    def reservar(self) -> None:
        """R3: pide al servicio crear la reserva."""
        self._accion(self.gym.realizar_reserva)

    def cancelar(self) -> None:
        """R7: pide al servicio cancelar la reserva."""
        self._accion(self.gym.cancelar_reserva)

    def confirmar(self) -> None:
        """R8: pide al servicio reactivar la reserva."""
        self._accion(self.gym.confirmar_reserva)

    def verificar_propietario(self) -> None:
        """R9 (método de Angelina): indica si el documento tiene alguna reserva."""
        respuesta = self.ejecutar(self.gym.verificar_propietario_reserva, self.documento.get().strip())
        if respuesta:
            self.resumen.config(text=f"¿La reserva pertenece al usuario?: {respuesta}.")

    def mostrar_resumen(self) -> None:
        """R10 (método de Angelina): muestra el resumen de la reserva del documento."""
        texto = self.ejecutar(self.gym.mostrar_resumen_reserva, self.documento.get().strip())
        if texto:
            self.resumen.config(text=texto)

    def consultar_disponibilidad(self) -> None:
        """R14 (método de Angelina): llena la tabla con (horario, estado, detalle) por horario."""
        filas = self.ejecutar(self.gym.consultar_disponibilidad, self.fecha.obtener())
        if filas is not None:
            self.tabla_disponibilidad.cargar(filas, [estado for _, estado, _ in filas])

    def refrescar(self) -> None:
        """Recarga la tabla de reservas registradas."""
        self.tabla_reservas.cargar([
            (r.nombre_usuario, r.documento, r.fecha, r.horario,
             "activa" if r.activa else "cancelada")
            for r in self.gym.listar_reservas()])
