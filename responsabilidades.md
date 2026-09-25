# Responsabilidades del proyecto — Gimnasio

Este documento define qué le corresponde a cada colaborador dentro de la nueva estructura del proyecto:

```
mi_proyecto/
├── modelos.py
├── excepciones.py
├── repositorios.py
├── servicios.py
└── main.py
```

---

## Samuel — Usuarios, Reservas y Ensamblaje final

### `modelos.py`
- Clase `Usuario`
- Clase `Reserva` (con sus métodos `cancelar()` y `confirmar()`)

### `repositorios.py`
- `UsuarioRepositorio` (ABC) + `UsuarioRepositorioMemoria`
- `ReservaRepositorio` (ABC) + `ReservaRepositorioMemoria`

### `servicios.py`
- `registrar_usuario()`
- `eliminar_usuario()`
- `realizar_reserva()` → **corregir bug:** `datetime.row()` debe ser `datetime.now()`
- `cancelar_reserva()`
- `confirmar_reserva()`

### `excepciones.py` (aporta)
- `DatoVacioError`
- `UsuarioNoRegistradoError`
- `UsuarioYaRegistradoError`

### `main.py` (responsabilidad adicional)
Una vez que Juan José y Angelina terminen sus repositorios y servicios, Samuel:
- Crea las instancias de los 4 repositorios.
- Construye el `GymService` inyectando todas las dependencias.
- Escribe un flujo de prueba de punta a punta (registrar usuario → reservar → registrar visita → dar prioridad), envuelto en `try/except GymError`.

---

## Juan José — Visitas y Estadísticas

### `modelos.py`
- Funciones utilitarias `es_bisiesto()` y `es_fecha_valida()`
- Clase `Visita`

### `repositorios.py`
- `VisitaRepositorio` (ABC) + `VisitaRepositorioMemoria`

### `servicios.py`
- `registrar_visita()`
- `horario_mas_frecuente()`
- `programa_mas_frecuente()`
- `promedio_duracion_por_usuario()`

### `excepciones.py` (aporta)
- `FechaInvalidaError`
- `DuracionInvalidaError`
- `HorarioInvalidoError`

---

## Angelina — Prioridades y Consultas de Reserva

### `modelos.py`
- Clase `Prioridad`

### `repositorios.py`
- `PrioridadRepositorio` (ABC) + `PrioridadRepositorioMemoria`

### `servicios.py`
- `prioridad_membresia()` → **corregir bug:** `self.tiempo_maximo` debe ser `self.duracion_maxima_sesion`
- `confirmar_prioridad()`
- `_liberar_prioridades_vencidas()`
- `verificar_propietario_reserva()`
- `mostrar_resumen_reserva()`

### `excepciones.py` (aporta)
- `PrioridadNoEncontradaError`
- `ReservaNoEncontradaError`
- `GymError` (clase base de la que heredan todas las demás excepciones)

