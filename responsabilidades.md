# Historias de Usuario y Plan de Trabajo (Entrega 2) – Gimnasio Universitario

El trabajo se reparte en tres módulos de 18 puntos de esfuerzo cada uno (33,3 % por integrante), con ramas por historia de usuario, revisión cruzada de cada pull request y una sustentación preparada desde el primer día.

**Proyecto:** Sistema de gestión de gimnasio universitario

**Asignatura:** Programación Orientada a Objetos · **Institución:** Universidad de Medellín

**Docente:** Mario Alejandro Saldarriaga Álvarez

**Equipo:** Juan José Aguirre Durango, Angelina Negrette Diaz, Samuel Zapata Trujillo

**Repositorio:** https://github.com/EntropyDip/gym_universitario.git

---

## 1. Lineamientos técnicos de la Entrega 2

La entrega pide diseño e implementación completa, manejo riguroso de excepciones, interfaz gráfica moderna y desacoplada, y modularización ejemplar. Estas directrices son de cumplimiento obligatorio:

- **Arquitectura por capas.** `modelos.py` (entidades del dominio y validación interna) → `repositorios.py` (almacenamiento abstracto e implementaciones en memoria) → `servicios.py` (lógica y orquestación de negocio en `GymService`) → `interfaz/` (capa de presentación exclusivamente).
- **La interfaz no contiene reglas de negocio.** Únicamente invoca métodos del servicio y funciones de lectura (`listar_*`, `consultar_disponibilidad`, `ocupantes_franja`); jamás accede ni muta las colecciones internas de forma directa.
- **Excepciones formales de dominio.** Toda infracción de una regla de negocio genera una excepción que hereda de `GymError`. La capa visual la intercepta y la despliega amigablemente mediante cuadros de diálogo (`messagebox.showerror`). Queda terminantemente prohibido el uso de `print` como mecanismo de control en modelos y servicios.
- **Hora inyectable y determinismo.** Aquellos métodos que dependen del tiempo aceptan `hora_actual` como parámetro opcional (por defecto, reloj del sistema), garantizando la reproducibilidad y aislamiento de las pruebas unitarias.
- **Capacidad por franja horaria (15 usuarios).** Cada turno de atención (franjas de 2 horas entre 08:00 AM y 08:00 PM) cuenta con un aforo máximo de 15 usuarios concurrentes (`capacidad_maxima = 15`), considerando de forma unificada reservas activas, visitas registradas y cupos con prioridad de membresía. Cuando se alcanza dicho límite, el sistema lanza `CupoLlenoError`.
- **Cómputo unificado de ocupantes.** Si un estudiante posee tanto reserva activa como asistencia registrada en la misma franja y fecha, se contabiliza como **un único cupo ocupado**.
- **Consistencia nominal con el documento de análisis.** Clases, atributos, excepciones y métodos conservan rigurosamente la nomenclatura descrita en las especificaciones del documento técnico.
- **Estilo y calidad de código.** Convención PEP 8 (`snake_case` para funciones/variables, `PascalCase` para clases), tipado estático asistido (`typing`), docstrings explicativos en cada módulo, clase y método público.
- **Librerías externas y degradación elegante.** `matplotlib` y `tkcalendar`, registradas en `requirements.txt`, con manejo de excepciones por importación para garantizar que la aplicación continúe operando si alguna no está presente.
- **Cobertura de pruebas unitarias.** Suite automatizada con `unittest` que cubre 58 pruebas en total, abarcando casos de éxito, bordes, límites de aforo y situaciones anómalas.
- **Público objetivo y roles de usuario:** El sistema es una aplicación administrativa de escritorio de uso exclusivo del **Administrador / Encargado** de la Universidad de Medellín, únicos encargados de manejar el programa (censo de usuarios, asignación/cancelación de reservas, registro de visitas, validación de prioridades y análisis de aforos, horarios pico, carreras más activas y desgaste de maquinaria). Los estudiantes no operan el sistema.

---

## 2. Matriz de distribución equitativa del trabajo

El proyecto comprende 15 requisitos funcionales formales distribuidos de manera equitativa: 5 requisitos por integrante (18 puntos de esfuerzo por persona, totalizando 54 puntos). Cada estudiante diseña e implementa la lógica de servicio, la capa visual de sus módulos y las respectivas pruebas unitarias.

| Integrante | Módulo | Requisitos asignados | Clases y componentes clave | Puntos |
|:---|:---|:---:|:---|:---:|
| **Samuel Zapata Trujillo** | Módulo 1: Usuarios, Reservas, Aforo y Ensamblaje | R1, R2, R3, R7, R8 | `Usuario`, `Reserva`, `UsuarioRepositorio`, `ReservaRepositorio`, `PanelUsuarios`, `PanelReservas`, control de aforo (15 cupos), `main.py` | 18 |
| **Juan José Aguirre Durango** | Módulo 2: Visitas, Calendario y Estadísticas | R4, R5, R6, R11, R15 | `es_bisiesto`, `es_fecha_valida`, `Visita`, `VisitaRepositorio`, `PanelVisitas`, `PanelEstadisticas` (KPIs y gráficos con `matplotlib`) | 18 |
| **Angelina Negrette Diaz** | Módulo 3: Prioridades, Consultas y Diseño de Interfaz | R9, R10, R12, R13, R14 | `Prioridad`, `PrioridadRepositorio`, `VentanaPrincipal`, `componentes.py`, `PanelPrioridades`, disponibilidad y ocupantes de franja, diagrama de clases UML | 18 |

- **Componentes compartidos:** `excepciones.py` (enriquecido con las excepciones de cada módulo), `test_gym.py` (cada integrante aporta las clases de prueba de su módulo hasta consolidar los 58 tests), `requirements.txt` y `README.md`.
- **Notificaciones por correo:** `notificador.py` envía la confirmación de reserva (R3 y R8) a los usuarios que tienen correo registrado, mediante SMTP de Gmail en un hilo secundario y con credenciales en las variables de entorno `GYM_EMAIL_REMITENTE` y `GYM_EMAIL_PASSWORD`; sin credenciales, el envío se omite sin errores.
- **Interoperabilidad:** El panel de reservas de Samuel consulta la disponibilidad y ocupantes desarrollados con Angelina (R14) e integra los botones de R9 y R10. El cálculo de prioridades de Angelina consulta el historial de visitas implementado por Juan José.

---

## 3. Metodología de trabajo en Git

### 3.1 Ramas por historia de usuario
Nadie realiza commits directamente sobre `main`. El desarrollo se estructura en ramas de características:

| Rama | Responsable | Descripción de alcance |
|---|---|---|
| `feature/HU-01-usuarios` | Samuel | Registro y eliminación en cascada de usuarios |
| `feature/HU-02-reservas` | Samuel | Reservas, cancelaciones, reactivaciones y aforo de 15 cupos |
| `feature/HU-03-interfaz-ensamblaje` | Samuel | `PanelUsuarios`, `PanelReservas`, CLI (`--demo`, `--consola`) y ensamblaje |
| `feature/HU-04-visitas` | Juan José | Registro de visitas, fecha opcional, prevención de duplicados y calendario gregoriano |
| `feature/HU-05-estadisticas` | Juan José | Horario/carrera pico, promedio de duración y ranking de maquinaria |
| `feature/HU-06-interfaz-visitas-estadisticas` | Juan José | `PanelVisitas`, `PanelEstadisticas` e integración visual con `matplotlib` |
| `feature/HU-07-consultas-reserva` | Angelina | Titularidad, resumen de reserva y disponibilidad con ocupantes de franja |
| `feature/HU-08-prioridades` | Angelina | Cupos preferenciales por fidelidad, límite de 2 horas y caducidad |
| `feature/HU-09-interfaz-diseno` | Angelina | `VentanaPrincipal`, `componentes.py`, `PanelPrioridades` y UML v2 |

### 3.2 Commits atómicos y verificación continua
- Commits granulares con formato convencional: `feat(reservas): validar aforo maximo de 15 usuarios`, `fix(prioridades): purgar cupos no confirmados a 2 horas`, `test(visitas): validar prevencion de visitas duplicadas`.
- Antes de cada integración se ejecuta la suite automatizada: `python -m unittest test_gym.py -v` y la verificación de flujo: `python main.py --consola`.

### 3.3 Revisión cruzada obligatoria
Nadie aprueba ni fusiona su propio Pull Request. El ciclo rotativo de revisión garantiza conocimiento cruzado:
- Samuel es revisado por Angelina.
- Juan José es revisado por Samuel.
- Angelina es revisada por Juan José.

---

## 4. Historias de Usuario y Criterios de Aceptación

### Responsable 1: Samuel Zapata Trujillo
**Módulo:** Usuarios, Reservas, Aforo y Ensamblaje

#### HU-01: Registro y eliminación de usuarios (5 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Registrar estudiantes con sus datos académicos y darlos de baja junto con sus registros asociados.
- **Para:** Mantener un censo oficial, limpio y sin duplicados en las instalaciones deportivas.
- **Requisitos:** R1, R2.
- **Criterios de aceptación:**
  1. El documento es único; un documento repetido lanza `UsuarioYaRegistradoError` sin alterar el repositorio.
  2. Nombre, documento o programa vacíos (o solo espacios) lanzan `DatoVacioError`.
  2.1. El correo electrónico es opcional; si se indica con formato inválido lanza `CorreoInvalidoError`, y si es válido se almacena en minúsculas.
  3. Eliminar con datos erróneos o inexistentes lanza `UsuarioNoRegistradoError`.
  4. Al eliminar un usuario por coincidencia de nombre y documento, se eliminan en cascada sus reservas, visitas y prioridades.
  5. Saneamiento automático de espacios en blanco (`strip()`).

#### HU-02: Reservas de cupos y control de aforo (8 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Reservar, cancelar y reactivar turnos en la agenda del gimnasio.
- **Para:** Garantizar el aforo ordenado de 15 cupos y asegurar el turno de entrenamiento sin depender de correos electrónicos.
- **Requisitos:** R3, R7, R8.
- **Criterios de aceptación:**
  1. Cada franja horaria admite hasta 15 usuarios concurrentes. Si se intenta reservar en una franja con 15 ocupantes, lanza `CupoLlenoError`.
  2. Un usuario no puede tener más de una reserva activa en la misma fecha ni más de 3 reservas activas en la misma semana calendario (`max_reservas_semana = 3`, `ReservaDuplicadaError`).
  3. Horarios no oficiales lanzan `HorarioInvalidoError`; fechas erróneas o irreales lanzan `FechaInvalidaError`.
  4. Quien ya cuenta con prioridad para la franja tiene su cupo garantizado; no requiere ni puede crear otra reserva (`ReservaDuplicadaError`).
  5. Cancelar una reserva activa libera inmediatamente 1 cupo para los demás usuarios. Si ya estaba cancelada, notifica sin generar error.
  6. Confirmar (reactivar) una reserva previamente cancelada verifica que la franja no esté llena (`CupoLlenoError`), que el usuario no tenga otra reserva activa ese día ni supere las 3 reservas semanales (`ReservaDuplicadaError`).
  7. Si el usuario tiene correo registrado, al reservar o reactivar se envía la confirmación por correo en un hilo secundario; sin credenciales configuradas, se omite sin afectar la operación.

#### HU-03: Interfaz de usuarios y reservas, y ensamblaje general (5 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Paneles gráficos para gestionar usuarios y reservas, y un punto de entrada flexible.
- **Para:** Operar el gimnasio intuitivamente y validar su funcionamiento en diferentes entornos.
- **Requisitos:** R1, R2, R3, R7, R8 (pantallas P1 y P2), ensamblaje en `main.py`.
- **Criterios de aceptación:**
  1. `PanelUsuarios` permite registrar y eliminar (con diálogo de confirmación) y refresca la tabla.
  2. `PanelReservas` permite reservar, cancelar, reactivar, consultar titularidad y ver resumen.
  3. `main.py` soporta ejecución estándar (`python main.py`), con datos precargados (`--demo`) y flujo automatizado (`--consola`).
  4. Todo error de negocio se muestra en diálogo modal sin abortar el proceso.

---

### Responsable 2: Juan José Aguirre Durango
**Módulo:** Visitas, Calendario y Estadísticas

#### HU-04: Registro de visitas y calendario gregoriano (5 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Registrar la asistencia real de cada estudiante indicando horario, duración y maquinaria utilizada.
- **Para:** Cuantificar el flujo real de deportistas y alimentar los modelos estadísticos institucionales.
- **Requisitos:** R4.
- **Criterios de aceptación:**
  1. Validación matemática de años bisiestos y días por mes (`es_bisiesto` y `es_fecha_valida`).
  2. El parámetro `fecha` es opcional; si no se especifica, toma la fecha actual del sistema.
  3. Duración debe ser un entero positivo entre 1 y 90 minutos (1:30 horas máximas, `DURACION_MAXIMA = 90`); valores negativos, cero, booleanos, no numéricos o que superen los 90 minutos lanzan `DuracionInvalidaError`.
  4. Un mismo estudiante no puede registrar dos visitas en la misma fecha y franja horaria (`VisitaDuplicadaError`).
  5. Las visitas se contabilizan en el aforo de 15 personas de la franja (`CupoLlenoError` si está llena). Quien tiene reserva y visita en el mismo turno cuenta una sola vez.
  6. Limpieza y saneamiento de la lista de equipos utilizados.

#### HU-05: Estadísticas de uso y analítica deportiva (8 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Conocer horarios pico, programas más frecuentes, tiempo promedio por usuario y ranking de maquinaria.
- **Para:** Tomar decisiones sobre mantenimiento preventivo de máquinas, dotación presupuestal y optimización de espacios.
- **Requisitos:** R5, R6, R11, R15.
- **Criterios de aceptación:**
  1. `horario_mas_frecuente` y `programa_mas_frecuente` devuelven la moda estadística, o mensaje claro si no hay datos.
  2. `promedio_duracion_por_usuario` calcula la media en minutos por usuario con un decimal.
  3. `datos_promedio_duracion` genera las tuplas numéricas ordenadas descendentemente para alimentar tablas y gráficos.
  4. `equipo_mas_utilizado` y `ranking_equipos` consolidan el uso de maquinaria normalizando nombres (insensible a mayúsculas/minúsculas).

#### HU-06: Interfaz de visitas y visualización analítica (5 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Una pantalla de captura rápida de visitas y un panel analítico con gráficos interactivos.
- **Para:** Monitorear el aforo del gimnasio en tiempo real y auditar métricas deportivas.
- **Requisitos:** R4, R5, R6, R11, R15 (pantallas P3 y P5).
- **Criterios de aceptación:**
  1. `PanelVisitas` ofrece casillas para equipos usuales y campo para máquinas adicionales.
  2. `PanelEstadisticas` muestra tarjetas de indicadores principales y dos gráficos de barras embebidos con `matplotlib` (duración media y ranking de equipos).
  3. Ante la ausencia de datos o de la librería `matplotlib`, el panel despliega avisos amigables sin generar excepciones no controladas.

---

### Responsable 3: Angelina Negrette Diaz
**Módulo:** Prioridades, Consultas y Diseño de Interfaz

#### HU-07: Consultas de titularidad, resumen y disponibilidad (5 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Saber si un estudiante tiene reservas, consultar su resumen y revisar qué horarios tienen cupos libres u ocupantes.
- **Para:** Atender oportunamente las consultas de los usuarios y verificar el estado del aforo en tiempo real.
- **Requisitos:** R9, R10, R14.
- **Criterios de aceptación:**
  1. `verificar_propietario_reserva` retorna «Sí» o «No» según la existencia de registros del documento.
  2. `mostrar_resumen_reserva` entrega la síntesis de la reserva más relevante; si no hay reservas, lanza `ReservaNoEncontradaError`.
  3. `consultar_disponibilidad` reporta cada horario con su estado: `LIBRE` (0/15), `PARCIAL` (1..14/15 con detalle de cupos libres) o `LLENO` (15/15).
  4. `ocupantes_franja` desglosa quiénes ocupan la franja seleccionada y bajo qué rol (Reserva, Visita o Prioridad).
  5. En `PanelReservas`, al hacer clic en una franja de la tabla de disponibilidad, se actualiza automáticamente la tabla de ocupantes contigua.

#### HU-08: Sistema dinámico de prioridades de membresía (8 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Apartar un cupo con exclusividad temporal para asegurar el turno de usuarios fieles o constantes.
- **Para:** Reconocer la disciplina deportiva y garantizar cupos conforme a las reglas de membresía.
- **Requisitos:** R12, R13.
- **Criterios de aceptación:**
  1. Se otorga prioridad si el usuario es "habitual" (≥3 visitas en ese mismo horario) o si acumula estrictamente más minutos que todos los demás usuarios (sin empates).
  2. Si no cumple los criterios de fidelidad, lanza `PrioridadNoCumpleError`.
  3. No puede solicitarse prioridad con menos de 2 horas de anticipación a la franja deseada (`PrioridadNoCumpleError`).
  4. La prioridad aparta 1 cupo garantizado (sujeto al aforo máximo de 15 personas). Otros estudiantes pueden continuar reservando los cupos restantes de la franja.
  5. La prioridad debe confirmarse con 2 o más horas de antelación (`confirmada = True`). Si se intenta confirmar tarde, la prioridad se purga y el cupo se libera de forma automática.
  6. `listar_prioridades_vigentes` depura automáticamente las prioridades caducadas antes de listarlas.

#### HU-09: Ventana principal, navegación y componentes base (5 puntos)
- **Como:** Administrador / Encargado.
- **Quiero:** Una interfaz gráfica organizada en pestañas, selectores amigables, identidad corporativa y un diseño documentado en UML.
- **Para:** Operar todos los módulos del gimnasio con facilidad, agilidad y consistencia visual institucional.
- **Requisitos:** P1 a P5, `VentanaPrincipal`, `componentes.py`, diagrama de clases UML.
- **Criterios de aceptación:**
  1. `VentanaPrincipal` integra el cuaderno de pestañas (`ttk.Notebook`), cabecera roja institucional de la Universidad de Medellín (`#D2232A`), logotipo corporativo (`interfaz/logo.png`), botones destacados en rojo (`#E0454C`) y refresco reactivo automático de paneles.
  2. `componentes.py` estandariza `PanelBase`, `TablaDatos` con scrollbar, `SelectorFecha` (con fallback de `tkcalendar`) y `SelectorHorario`.
  3. Diagrama de clases UML actualizado reflejando la arquitectura por capas, las entidades, `GymService`, repositorios y la jerarquía de 13 excepciones.

---

## 5. Dependencias y Orden de Integración

```text
       ┌──────────────┐     ┌──────────────┐
       │ HU-01 (Samuel)│     │HU-04(Juan Jo)│
       │   Usuarios   │     │   Visitas    │
       └──────┬───────┘     └──────┬───────┘
              │                    │
              ├──────────┬─────────┤
              ▼          ▼         ▼
       ┌──────────────┐  │  ┌──────────────┐
       │ HU-02 (Samuel)│  │  │HU-05(Juan Jo)│
       │   Reservas   │  │  │ Estadísticas │
       └──────┬───────┘  │  └──────────────┘
              │          ▼
              │   ┌──────────────┐
              │   │HU-08(Angelina│
              │   │ Prioridades  │
              │   └──────┬───────┘
              ▼          ▼
       ┌─────────────────────────┐
       │    HU-07 (Angelina)     │
       │Consultas, Disponibilidad│
       └────────────┬────────────┘
                    ▼
       ┌─────────────────────────┐
       │  HU-03 / HU-06 / HU-09  │
       │Interfaz Gráfica Integral│
       └─────────────────────────┘
```

1. **Fase 1 (Paralela):** HU-01 (Usuarios) y HU-04 (Visitas y validación de calendario).
2. **Fase 2:** HU-02 (Reservas y aforo de 15 cupos), HU-05 (Estadísticas analíticas) y HU-08 (Prioridades de membresía).
3. **Fase 3:** HU-07 (Consultas de titularidad, resumen y disponibilidad con ocupantes).
4. **Fase 4 (Ensamblaje final):** HU-03, HU-06 y HU-09 (Integración en `VentanaPrincipal`, componentes reutilizables, CLI y datos demo).

---

## 6. Plan de Verificación y Validación Conjunta

La verificación del sistema se realiza en dos etapas formales:

### Etapa 1: Suite Automatizada de Pruebas Unitarias (58 tests)
Ejecución: `python -m unittest test_gym.py -v`
- [x] 14 pruebas de aforo y concurrencia (`TestCapacidadPorFranja`).
- [x] 11 pruebas de prioridades y caducidad temporal (`TestPrioridades`).
- [x] 7 pruebas de ciclo de vida de reservas (`TestReservas`).
- [x] 10 pruebas de gestión de usuarios (incluido el correo opcional) y purga en cascada (`TestUsuarios`).
- [x] 6 pruebas de visitas, fechas gregorianas y años bisiestos (`TestVisitasYFechas`).
- [x] 4 pruebas de analítica y métricas estadísticas (`TestEstadisticas`).
- [x] 3 pruebas de consultas y disponibilidad (`TestConsultasYDisponibilidad`).
- [x] 3 pruebas de saneamiento de espacios y purga reactiva (`TestEspaciosEnFechasYPrioridadesVigentes`).

### Etapa 2: Recorrido del Flujo de Punta a Punta en Consola e Interfaz
Ejecución: `python main.py --consola` seguido de `python main.py --demo`
- [x] **Paso 1 (Samuel y Juan José):** Registrar usuarios, validar unicidad de documento, registrar visitas con fecha explícita u omitida, comprobar `DuracionInvalidaError` (≤0 o >90 min) y `VisitaDuplicadaError`.
- [x] **Paso 2 (Samuel):** Realizar reserva, validar límite de 1 reserva activa por fecha y máximo 3 reservas semanales (`ReservaDuplicadaError`), cancelar y confirmar reactivación.
- [x] **Paso 3 (Juan José y Angelina):** Registrar ≥3 visitas en un mismo horario, solicitar prioridad de membresía y confirmar con antelación superior a 2 horas.
- [x] **Paso 4 (Angelina y Samuel):** Comprobar que otros usuarios pueden reservar en la misma franja mientras haya cupos libres (< 15).
- [x] **Paso 5 (Angelina):** Intentar confirmar una prioridad pasada la ventana de 2 horas previas y comprobar la liberación automática del cupo.
- [x] **Paso 6 (Samuel):** Llenar una franja con 15 usuarios (combinando reservas, visitas y prioridades) y comprobar que el intento 16 lanza `CupoLlenoError`.
- [x] **Paso 7 (Juan José):** Consultar horario pico, programa académico más frecuente, duración media por usuario y ranking ordenado de maquinaria deportiva.
- [x] **Paso 8 (Angelina):** Consultar disponibilidad (LIBRE, PARCIAL, LLENO) y seleccionar una franja para inspeccionar la tabla de ocupantes en tiempo real.
- [x] **Paso 9 (Samuel):** Eliminar un usuario con reservas, visitas y prioridades activas, y verificar que todas sus entidades son purgadas en cascada de forma inmediata.
- [x] **Paso 10 (Los tres):** Abrir cada pestaña en la interfaz gráfica (`python main.py`), provocar intencionalmente errores de negocio y verificar que se interceptan mediante diálogos modales sin cerrar la aplicación.
