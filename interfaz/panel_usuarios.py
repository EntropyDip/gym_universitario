"""Pantalla P1: registro y eliminación de usuarios (R1, R2)."""
from tkinter import messagebox, ttk

from interfaz.componentes import PanelBase, TablaDatos


class PanelUsuarios(PanelBase):
    """Formulario para registrar y eliminar usuarios, con la tabla de usuarios."""

    def __init__(self, master, gym):
        super().__init__(master, gym)
        formulario = ttk.LabelFrame(self, text="Usuario")
        formulario.pack(fill="x", padx=10, pady=8)

        self.campos = {}
        for fila, (clave, texto) in enumerate((("nombre", "Nombre"),
                                               ("documento", "Documento"),
                                               ("programa", "Programa académico"))):
            ttk.Label(formulario, text=texto).grid(row=fila, column=0, padx=5, pady=4, sticky="w")
            self.campos[clave] = ttk.Entry(formulario, width=35)
            self.campos[clave].grid(row=fila, column=1, padx=5, pady=4)

        # Campo correo electrónico (opcional) — para notificaciones de reserva
        ttk.Label(formulario, text="Correo electrónico").grid(
            row=3, column=0, padx=5, pady=4, sticky="w")
        self.campos["correo"] = ttk.Entry(formulario, width=35)
        self.campos["correo"].grid(row=3, column=1, padx=5, pady=4)
        ttk.Label(formulario, text="(opcional — recibirá confirmación de reserva)",
                  foreground="#666").grid(row=3, column=2, padx=5, sticky="w")

        botones = ttk.Frame(formulario)
        botones.grid(row=4, column=0, columnspan=3, pady=6)
        ttk.Button(botones, text="Registrar", command=self.registrar).pack(side="left", padx=5)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)

        self.tabla = TablaDatos(self, ["Nombre", "Documento", "Programa", "Correo"])
        self.tabla.pack(fill="both", expand=True, padx=10, pady=8)
        self.refrescar()

    def _leer(self) -> tuple[str, str, str, str]:
        """Lee los campos del formulario incluyendo el correo."""
        return (self.campos["nombre"].get(), self.campos["documento"].get(),
                self.campos["programa"].get(), self.campos["correo"].get())

    def _limpiar(self) -> None:
        """Vacía los campos del formulario."""
        for campo in self.campos.values():
            campo.delete(0, "end")

    def registrar(self) -> None:
        """Pide al servicio registrar el usuario y muestra el mensaje o el error."""
        nombre, documento, programa, correo = self._leer()
        mensaje = self.ejecutar(self.gym.registrar_usuario, nombre, documento, programa, correo)
        if mensaje:
            messagebox.showinfo("Usuarios", mensaje)
            self._limpiar()
            self.refrescar()

    def eliminar(self) -> None:
        """Pide confirmación y pide al servicio eliminar al usuario (nombre y documento)."""
        nombre, documento, _, _ = self._leer()
        if not messagebox.askyesno(
                "Confirmar", "¿Eliminar al usuario con todas sus reservas, visitas y prioridades?"):
            return
        mensaje = self.ejecutar(self.gym.eliminar_usuario, nombre, documento)
        if mensaje:
            messagebox.showinfo("Usuarios", mensaje)
            self._limpiar()
            self.refrescar()

    def refrescar(self) -> None:
        """Recarga la tabla de usuarios."""
        self.tabla.cargar([(u.nombre, u.documento, u.programa, u.correo or "—")
                           for u in self.gym.listar_usuarios()])
