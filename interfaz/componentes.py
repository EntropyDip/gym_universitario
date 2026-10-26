"""Componentes base reutilizables para la interfaz gráfica (Angelina - HU-09)."""
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk

from excepciones import GymError


class PanelBase(ttk.Frame):
    """Clase base de todos los paneles de la interfaz gráfica."""

    def __init__(self, master, gym) -> None:
        super().__init__(master)
        self.gym = gym

    def ejecutar(self, metodo, *args):
        """Ejecuta una acción del servicio capturando y mostrando cualquier error de negocio."""
        try:
            return metodo(*args)
        except GymError as error:
            messagebox.showerror("Error de negocio", str(error))
            return None
        except Exception as error:
            messagebox.showerror("Error inesperado", f"{type(error).__name__}: {error}")
            return None

    def refrescar(self) -> None:
        """Método opcional que los paneles sobreescriben para actualizar sus datos."""
        pass


class TablaDatos(ttk.Frame):
    """Componente reutilizable de tabla basado en Treeview con barra de desplazamiento."""

    def __init__(self, master, encabezados: list[str], alto: int = 8) -> None:
        super().__init__(master)
        self.columnas = [f"c{i}" for i in range(len(encabezados))]
        self.arbol = ttk.Treeview(
            self,
            columns=self.columnas,
            show="headings",
            height=alto,
            selectmode="browse"
        )
        barra_v = ttk.Scrollbar(self, orient="vertical", command=self.arbol.yview)
        self.arbol.configure(yscrollcommand=barra_v.set)

        for col, texto in zip(self.columnas, encabezados):
            self.arbol.heading(col, text=texto)
            self.arbol.column(col, anchor="center", stretch=True, width=120)

        self.arbol.pack(side="left", fill="both", expand=True)
        barra_v.pack(side="right", fill="y")

    def cargar(self, filas: list[tuple], etiquetas_color: list[str] | None = None) -> None:
        """Limpia y vuelve a cargar los datos en la tabla."""
        for item in self.arbol.get_children():
            self.arbol.delete(item)

        for indice, fila in enumerate(filas):
            tags = ()
            if etiquetas_color and indice < len(etiquetas_color):
                tags = (etiquetas_color[indice],)
            self.arbol.insert("", "end", values=fila, tags=tags)

    def colorear(self, mapa_colores: dict[str, str]) -> None:
        """Asigna colores de fondo según las etiquetas asignadas a las filas."""
        for etiqueta, color in mapa_colores.items():
            self.arbol.tag_configure(etiqueta, background=color)


class SelectorFecha(ttk.Frame):
    """Selector de fecha que utiliza tkcalendar si está disponible o un campo de texto asistido."""

    def __init__(self, master, dias_inicial: int = 1) -> None:
        super().__init__(master)
        inicial = datetime.now() + timedelta(days=dias_inicial)
        fecha_inicial = inicial.strftime("%Y-%m-%d")
        self.usa_tkcalendar = False

        try:
            from tkcalendar import DateEntry
            self.calendario = DateEntry(
                self,
                date_pattern="yyyy-mm-dd",
                width=12,
                background="darkblue",
                foreground="white",
                headersbackground="lightblue"
            )
            self.calendario.set_date(inicial)
            self.calendario.pack(side="left")
            self.usa_tkcalendar = True
        except ImportError:
            self.entrada = ttk.Entry(self, width=13)
            self.entrada.insert(0, fecha_inicial)
            self.entrada.pack(side="left")

    def obtener(self) -> str:
        """Devuelve la fecha seleccionada en formato AAAA-MM-DD."""
        if self.usa_tkcalendar:
            return str(self.calendario.get_date().strftime("%Y-%m-%d"))
        return self.entrada.get().strip()


class SelectorHorario(ttk.Frame):
    """Selector de horario basado en un Combobox de solo lectura."""

    def __init__(self, master, horarios: list[str]) -> None:
        super().__init__(master)
        self.variable = tk.StringVar()
        self.combo = ttk.Combobox(
            self,
            textvariable=self.variable,
            values=list(horarios),
            state="readonly",
            width=15
        )
        if horarios:
            self.combo.current(0)
        self.combo.pack(side="left")

    def obtener(self) -> str:
        """Devuelve el horario seleccionado."""
        return self.variable.get().strip()

    def obtener(self) -> str:
        """Devuelve la fecha seleccionada en formato AAAA-MM-DD."""
        if self.usa_tkcalendar:
            return str(self.calendario.get_date().strftime("%Y-%m-%d"))
        return self.entrada.get().strip()
