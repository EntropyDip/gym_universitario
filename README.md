# Sistema de Gestión de Gimnasio Universitario

Sistema desarrollado en Python bajo el paradigma de **Programación Orientada a Objetos** con una **arquitectura por capas desacoplada** para la administración integral de usuarios, reservas, visitas y prioridades de un gimnasio universitario, **concebido exclusivamente para el uso del Administrador o Encargado del gimnasio, quienes son los únicos que manejan el programa**.

Permite registrar estudiantes, gestionar reservas con control de aforo por franja horaria (hasta 15 usuarios simultáneos), llevar un registro detallado de visitas y maquinaria deportiva utilizada, fidelizar usuarios habituales con cupos prioritarios temporizados y generar analíticas y estadísticas en tiempo real con gráficos interactivos.

### Actores del Sistema
- **Administrador / Encargado:** único actor y usuario exclusivo del software. Gestiona el censo de estudiantes, la programación, cancelación y reactivación de reservas, el registro de asistencias reales (visitas), la verificación de disponibilidad, el trámite de prioridades de membresía y el análisis de las métricas de rendimiento deportivo (horarios pico, programas con mayor demanda, tiempo de permanencia y ranking de uso de maquinaria).

Los estudiantes no operan el sistema: son entidades del dominio (`Usuario`) cuyos datos y solicitudes son gestionados por el Administrador / Encargado. El actor de todos los requisitos funcionales (R1 a R15) es el **Administrador / Encargado**.

---

## Arquitectura del Sistema

El proyecto sigue una estricta separación de responsabilidades en cuatro capas:

```text
gym_universitario/
│
├── modelos.py           # Capa de Dominio: Entidades (Usuario, Reserva, Visita, Prioridad) y validación matemática de fechas
├── repositorios.py      # Capa de Persistencia: Contratos abstractos (ABC) e implementaciones en memoria
├── servicios.py         # Capa de Negocio: GymService (orquestador de los 15 requisitos funcionales)
├── notificador.py       # Notificaciones por correo electrónico (confirmación de reserva vía SMTP)
├── excepciones.py       # Jerarquía formal de errores de dominio (heredan de GymError)
├── interfaz/            # Capa de Presentación: GUI desacoplada en Tkinter/ttk con gráficos embebidos
│   ├── componentes.py       # Widgets reutilizables (PanelBase, TablaDatos, SelectorFecha, SelectorHorario)
│   ├── logo.png             # Logotipo institucional (Universidad de Medellín)
│   ├── ventana_principal.py # Ventana raíz contenedora con cabecera roja institucional (#D2232A) y pestañas
│   ├── panel_usuarios.py    # Pantalla P1: Usuarios (R1, R2)
│   ├── panel_reservas.py    # Pantalla P2: Reservas y Disponibilidad (R3, R7, R8, R9, R10, R14)
│   ├── panel_visitas.py     # Pantalla P3: Asistencia y Equipos (R4)
│   ├── panel_prioridades.py # Pantalla P4: Fidelización y Caducidad (R12, R13)
│   └── panel_estadisticas.py# Pantalla P5: Métricas y Gráficos Matplotlib (R5, R6, R11, R15)
│
├── main.py              # Punto de entrada, inyección de dependencias y CLI (--demo, --consola)
├── test_gym.py          # Suite completa de 58 pruebas unitarias automatizadas con unittest
├── requirements.txt     # Librerías externas (matplotlib, tkcalendar)
├── responsabilidades.md # Plan de trabajo, historias de usuario y matriz de distribución
└── GYM_UNIVERSITARIO (1).md # Informe técnico maestro de análisis y diseño integral
```

---

## Entidades del Dominio

1. **`Usuario`**: representa al estudiante inscrito en el gimnasio (nombre, número de documento, programa académico y correo electrónico opcional). Es registrado y gestionado por el Administrador / Encargado; no opera el sistema.
2. **`Reserva`**: representa el apartado de un cupo en un horario y fecha específicos (documento, nombre, horario, fecha, estado activo/cancelado). Cuenta con métodos para cancelar, confirmar/reactivar, comprobar titularidad y emitir resumen.
3. **`Visita`**: registra la asistencia física y el uso efectivo de las instalaciones (documento, horario, duración en minutos entre 1 y 90, fecha y lista de equipos utilizados).
4. **`Prioridad`**: representa un cupo exclusivo apartado preventivamente por un usuario de alta fidelidad (documento, nombre, horario, fecha, marca temporal de solicitud y estado de confirmación).
5. **`GymService`**: orquestador central que administra las colecciones mediante repositorios inyectados, valida las reglas de negocio, controla el límite de hasta 3 reservas activas semanales (`max_reservas_semana = 3`), gestiona el aforo máximo de 15 usuarios por franja y la agenda de turnos operativos (**08:00 AM a 08:00 PM**, cada 2 horas).

---

## Requisitos Funcionales Implementados (R1 a R15)

| ID | Operación / Método | Tipo | Descripción |
|:---:|---|:---:|---|
| **R1** | `registrar_usuario` | Tipo 1 | Registra un nuevo estudiante validando formato de texto, unicidad de documento y, si se indica, el formato del correo electrónico opcional (`CorreoInvalidoError`). |
| **R2** | `eliminar_usuario` | Tipo 1 | Da de baja a un usuario validando coincidencia de nombre y documento, ejecutando la purga transaccional en cascada de sus reservas, visitas y prioridades *(Innovación Samuel Zapata)*. |
| **R3** | `realizar_reserva` | Tipo 1 | Aparta un cupo en una fecha y franja horaria válida. Controla el límite de una reserva activa diaria, máximo 3 reservas activas semanales por estudiante y el aforo máximo de 15 usuarios por franja. Si el usuario tiene correo registrado, se envía la confirmación por correo electrónico en un hilo secundario; si no hay credenciales configuradas, la notificación se omite sin interrumpir la reserva. |
| **R4** | `registrar_visita` | Tipo 1 | Registra la asistencia efectiva, duración (1 a 90 min / 1:30 horas) y máquinas usadas. Fecha opcional (toma hoy por defecto) y previene visitas duplicadas en la misma franja y fecha. |
| **R5** | `horario_mas_frecuente` | Tipo 2 | Calcula la franja horaria con mayor afluencia de visitas. |
| **R6** | `programa_mas_frecuente` | Tipo 2 | Calcula la carrera universitaria con mayor número de estudiantes registrados. |
| **R7** | `cancelar_reserva` | Tipo 1 | Cambia el estado de una reserva activa a cancelada, liberando inmediatamente un cupo en la franja. |
| **R8** | `confirmar_reserva` | Tipo 1 | Reactiva una reserva previamente cancelada, validando aforo de 15, que el usuario no tenga otra reserva activa ese día ni supere las 3 reservas semanales *(Innovación Samuel Zapata)*. Si el usuario tiene correo registrado, se envía la confirmación de la reserva reactivada por correo electrónico en un hilo secundario; si no hay credenciales configuradas, la notificación se omite sin interrumpir la reserva. |
| **R9** | `verificar_propietario_reserva` | Tipo 2 | Retorna «Sí» si el usuario cuenta con al menos una reserva (activa o histórica) en el sistema, o «No». |
| **R10** | `mostrar_resumen_reserva` | Tipo 2 | Emite una síntesis textual detallada de la reserva más relevante del estudiante. |
| **R11** | `promedio_duracion_por_usuario` | Tipo 2 | Calcula la duración media de permanencia por estudiante con precisión de un decimal *(Innovación Juan José Aguirre)*. |
| **R12** | `prioridad_membresia` | Tipo 1 | Otorga un cupo prioritario a usuarios habituales (≥3 visitas en esa franja) o con mayor tiempo acumulado (sin empates), con ventana límite de 2 horas antes de la sesión *(Innovación Angelina Negrette)*. |
| **R13** | `confirmar_prioridad` | Tipo 3 | Confirma la asistencia a una prioridad antes del límite de 2 horas previas; si caduca, la prioridad se purga y el cupo se libera automáticamente *(Innovación Angelina Negrette)*. |
| **R14** | `consultar_disponibilidad` / `ocupantes_franja` | Tipo 2 | Consulta el estado del aforo (LIBRE, PARCIAL o LLENO) de todas las franjas horarias y lista de forma unificada los ocupantes de cada franja (reservas, visitas y prioridades). |
| **R15** | `equipo_mas_utilizado` / `ranking_equipos` | Tipo 2 | Determina la maquinaria con mayor índice de utilización y genera el ranking general descendente para gráficos interactivos *(Innovación Juan José Aguirre)*. |

---

## Reglas del Negocio y Restricciones Técnicas

1. **Capacidad Máxima de 15 Usuarios por Franja**: Cada horario operativo (08:00 AM a 08:00 PM) admite un aforo máximo de 15 personas (`capacidad_maxima = 15`), contabilizando de forma unificada reservas activas, asistencias registradas y prioridades otorgadas. Si se intenta exceder el aforo, se lanza `CupoLlenoError`.
2. **Cómputo Unificado de Ocupantes**: Si un estudiante tiene reserva y visita registrada en la misma franja y fecha, cuenta como **un único cupo ocupado**.
3. **Límite Diario y Semanal de Reservas**: Un usuario solo puede tener una reserva activa por fecha y hasta un máximo de 3 reservas activas por semana calendario bajo la norma ISO (`max_reservas_semana = 3`, `ReservaDuplicadaError`).
4. **Validación de Calendario Gregoriano**: Las fechas deben ingresar en formato estricto `AAAA-MM-DD` y se valida matemáticamente su existencia real, incluyendo años bisiestos (`es_bisiesto` y `es_fecha_valida`).
5. **No Duplicidad de Documentos**: No se permiten documentos duplicados en el registro de usuarios (`UsuarioYaRegistradoError`).
   - El correo electrónico del usuario es opcional; si se proporciona, se normaliza a minúsculas y debe tener formato válido (`CorreoInvalidoError`).
6. **No Duplicidad de Visitas en la Misma Franja**: Un estudiante no puede tener registradas dos visitas en la misma fecha y horario (`VisitaDuplicadaError`).
7. **Sesión de Visita Válida**: La duración debe ser un número entero estrictamente mayor a 0 y menor o igual a 90 minutos (`DURACION_MAXIMA = 90`, correspondiente a 1:30 horas máximas, `DuracionInvalidaError`).
8. **Condiciones de Prioridad y Caducidad**:
   - Para solicitar prioridad, el usuario debe tener ≥3 visitas históricas en ese mismo horario o acumular estrictamente más minutos que cualquier otro usuario (sin empates).
   - No puede solicitarse prioridad con menos de 2 horas de antelación respecto a la franja deseada.
   - La prioridad debe confirmarse con al menos 2 horas de anticipación. De lo contrario, caduca y se libera automáticamente.
   - La prioridad aparta 1 cupo garantizado para el estudiante, sin bloquear los cupos restantes de la franja.
9. **Eliminación Transaccional en Cascada**: Dar de baja a un usuario purga de manera automática e inmediata todas sus reservas, visitas históricas y prioridades.
10. **Desacoplamiento Absoluto Vista-Dominio e Identidad Visual**: La interfaz gráfica (`tkinter`/`ttk`) no contiene reglas de negocio; incorpora la identidad visual institucional de la Universidad de Medellín (cabecera `#D2232A` con logotipo y botones `#E0454C`), captura las excepciones de dominio (`GymError`) y las presenta mediante cuadros de diálogo sin interrumpir la ejecución.

---

## Jerarquía de Excepciones de Dominio

Todas las excepciones heredan de la clase base `GymError`:

- `DatoVacioError`: Campo obligatorio vacío o compuesto únicamente por espacios.
- `FechaInvalidaError`: Fecha no existente en el calendario gregoriano o con formato erróneo.
- `DuracionInvalidaError`: Duración de visita menor o igual a cero, no numérica o superior a 90 minutos (1:30 horas).
- `UsuarioNoRegistradoError`: Documento no encontrado o nombre no coincidente al eliminar.
- `UsuarioYaRegistradoError`: Intento de registrar un documento ya existente.
- `HorarioInvalidoError`: Franja horaria no perteneciente a la agenda oficial.
- `ReservaNoEncontradaError`: Intento de operar sobre una reserva inexistente.
- `ReservaDuplicadaError`: Intento de registrar dos reservas activas el mismo día, más de 3 reservas en la misma semana o reservar cuando ya se tiene prioridad en la franja.
- `PrioridadNoCumpleError`: Solicitud de prioridad sin cumplir visitas mínimas (≥3), sin mayor tiempo acumulado o con menos de 2 horas de antelación.
- `PrioridadNoEncontradaError`: Intento de confirmar una prioridad no registrada.
- `CupoLlenoError`: Franja horaria que ya alcanzó los 15 usuarios máximos permitidos.
- `VisitaDuplicadaError`: Intento de registrar dos visitas para el mismo estudiante en la misma fecha y franja horaria.
- `CorreoInvalidoError`: Correo electrónico con formato no válido al registrar un usuario.

---

## Requisitos e Instalación

### Requisitos previos
- **Python 3.10 o superior**
- Sistema Operativo: Windows, macOS o Linux

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

*Contenido de `requirements.txt`:*
```text
matplotlib>=3.8.0
tkcalendar>=1.6.1
```

> [!NOTE]
> La aplicación cuenta con mecanismos de degradación elegante (fallbacks automáticos): si `tkcalendar` no está instalado, habilita un campo de texto asistido; si `matplotlib` no está instalado, la pantalla de estadísticas muestra los indicadores numéricos y notifica la ausencia de la librería sin romper la ejecución.

---

## Notificaciones por Correo Electrónico (opcional)

El módulo `notificador.py` envía un correo de confirmación cuando se realiza o se reactiva una reserva de un usuario que tiene correo registrado. El envío se hace en un hilo secundario mediante el servidor SMTP de Gmail (`smtp.gmail.com:587`, STARTTLS), por lo que no bloquea la interfaz. Las credenciales se leen de variables de entorno, sin exponer contraseñas en el código:

```bash
# Linux / macOS
export GYM_EMAIL_REMITENTE="gimnasio@gmail.com"
export GYM_EMAIL_PASSWORD="contraseña-de-aplicación-de-gmail"

# Windows (PowerShell)
$env:GYM_EMAIL_REMITENTE="gimnasio@gmail.com"
$env:GYM_EMAIL_PASSWORD="contraseña-de-aplicación-de-gmail"
```

Si las variables no están definidas, el módulo trabaja en modo silencioso: informa en consola y omite el envío sin interrumpir la reserva.

---

## Modos de Ejecución

El archivo `main.py` incorpora soporte completo por línea de comandos para tres modalidades de uso:

### 1. Interfaz Gráfica Limpia (Por defecto)
Inicia la aplicación con las colecciones vacías, lista para operación real reactiva:
```bash
python main.py
```

### 2. Interfaz Gráfica con Datos Demo Precargados
Inicia la aplicación con un conjunto completo de usuarios, visitas históricas, reservas y prioridades para demostración y sustentación:
```bash
python main.py --demo
```

### 3. Flujo Completo de Consola (R1 a R15 + Pruebas de Aforo)
Ejecuta de punta a punta en la terminal todos los requisitos funcionales, validaciones y manejo de excepciones:
```bash
python main.py --consola
```

---

## Pruebas Unitarias Automatizadas

El sistema cuenta con una batería de **58 pruebas unitarias automatizadas** implementadas con la biblioteca estándar `unittest`:

```bash
python -m unittest test_gym.py -v
```

### Cobertura de las 58 Pruebas:
- **`TestCapacidadPorFranja` (14 pruebas)**: Límite de aforo de 15 usuarios por franja, reserva número 16 rechazada con `CupoLlenoError`, liberación de cupos al cancelar, reactivación en franja llena, visitas como ocupantes, cómputo único por estudiante multirrol, visitante 16 rechazado, prevención de visitas duplicadas con `VisitaDuplicadaError`, visitas en diferentes franjas o fechas, visitas con fecha hoy por defecto, prioridad como cupo ocupado y desestimación de prioridad innecesaria para quien ya tiene reserva activa.
- **`TestPrioridades` (11 pruebas)**: Prioridad por usuario habitual (≥3 visitas), rechazo por incumplimiento de requisitos, reserva concurrente de franja con prioridad ajena, confirmación a tiempo, liberación automática por confirmación tardía, búsqueda inexistente, rechazo con menos de 2 horas de antelación, prioridad por mayor tiempo acumulado, bloqueo de reserva redundante al titular de la prioridad, reflejo de prioridad en disponibilidad y validación de datos vacíos.
- **`TestReservas` (7 pruebas)**: Reserva exitosa, rechazo por usuario no registrado, franja inválida, fecha inválida o año no bisiesto, doble reserva activa en el mismo día, ciclo completo de cancelación/reactivación y cancelación de reserva inexistente.
- **`TestUsuarios` (10 pruebas)**: Registro exitoso, duplicados rechazados, campos vacíos o solo espacios, correo válido almacenado, correo inválido rechazado con `CorreoInvalidoError`, correo omitido (opcional), saneamiento de espacios en documento, eliminación inexistente, eliminación con nombre incorrecto y eliminación en cascada atómica (usuarios, reservas, visitas y prioridades).
- **`TestVisitasYFechas` (6 pruebas)**: Registro exitoso de visita, duración inválida (cero, negativa o booleano), usuario no registrado, franja inválida, algoritmo matemático de años bisiestos y validador de calendario gregoriano.
- **`TestEstadisticas` (4 pruebas)**: Horario pico más frecuente, carrera académica más frecuente, promedio de duración en minutos por estudiante y comportamiento con repositorios vacíos.
- **`TestConsultasYDisponibilidad` (3 pruebas)**: Verificación de titularidad de reserva (Sí/No), resumen textual de reserva y consulta de estados de disponibilidad.
- **`TestEspaciosEnFechasYPrioridadesVigentes` (3 pruebas)**: Cancelación con espacios accidentales en la fecha, solicitud de prioridad con espacios y purga reactiva de prioridades vencidas.

---

## Equipo de Desarrollo

Proyecto desarrollado para la asignatura **Programación Orientada a Objetos** en la **Universidad de Medellín** (2026), docente **Mario Alejandro Saldarriaga Álvarez**.

- **Samuel Zapata Trujillo** — Módulo 1: Usuarios, Reservas, Aforo y Ensamblaje (`main.py`, `PanelUsuarios`, `PanelReservas`, R1, R2, R3, R7, R8).
- **Juan José Aguirre Durango** — Módulo 2: Visitas, Calendario y Estadísticas Analíticas (`PanelVisitas`, `PanelEstadisticas`, R4, R5, R6, R11, R15).
- **Angelina Negrette Diaz** — Módulo 3: Prioridades, Consultas y Diseño de Interfaz (`VentanaPrincipal`, `componentes.py`, `PanelPrioridades`, R9, R10, R12, R13, R14).
