# Sistema de Gestión de Gimnasio Universitario

Sistema desarrollado en Python bajo el paradigma de **Programación Orientada a Objetos** con una **arquitectura por capas desacoplada** para la administración integral de usuarios, reservas, visitas y prioridades de un gimnasio universitario, **diseñado específicamente para el uso del encargado de las reservas y el jefe de deportes**.

Permite registrar estudiantes, gestionar reservas con control de aforo por franja horaria (hasta 15 usuarios simultáneos), llevar un registro detallado de visitas y maquinaria deportiva utilizada, fidelizar usuarios habituales con cupos prioritarios temporizados y generar analíticas y estadísticas en tiempo real con gráficos interactivos.

### Roles de Usuario del Sistema
- **Encargado de las reservas:** perfil operativo que gestiona en el mostrador/recepción el censo de estudiantes, la programación y reactivación de reservas, el registro de asistencias reales (visitas), la verificación de disponibilidad y el trámite de prioridades de membresía.
- **Jefe de deportes:** perfil supervisor y estratégico que audita la agenda y aforos, y analiza las métricas de rendimiento deportivo (horarios pico, programas con mayor demanda, tiempo de permanencia y ranking de uso de maquinaria) para planificar mantenimiento y optimizar recursos.

---

## Arquitectura del Sistema

El proyecto sigue una estricta separación de responsabilidades en cuatro capas:

```text
gym_universitario/
│
├── modelos.py           # Capa de Dominio: Entidades (Usuario, Reserva, Visita, Prioridad) y validación matemática de fechas
├── repositorios.py      # Capa de Persistencia: repositorios en memoria y contactos JSON
├── servicios.py         # Capa de Negocio: GymService (orquestador de los 15 requisitos funcionales)
├── notificador.py       # Notificaciones por correo con fallback SMS/WhatsApp
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
├── usuarios.json        # Contactos de usuarios (generado en ejecución y excluido de Git)
├── test_gym.py          # Pruebas unitarias de las reglas de negocio
├── test_contactos_notificaciones.py # Pruebas de persistencia JSON y notificaciones
├── requirements.txt     # Librerías externas (matplotlib, tkcalendar)
├── responsabilidades.md # Plan de trabajo, historias de usuario y matriz de distribución
└── GYM_UNIVERSITARIO (1).md # Informe técnico maestro de análisis y diseño integral
```

---

## Persistencia de contactos y notificaciones

La aplicación de escritorio crea `usuarios.json` en la carpeta del proyecto.
El archivo contiene únicamente una lista de objetos con `identificador` (el
documento del usuario), `correo` y `celular`; no almacena contraseñas ni datos
académicos. Las escrituras reemplazan el JSON de forma atómica y los errores de
lectura, formato o escritura se muestran como errores de persistencia. El archivo
está excluido de Git para proteger los datos personales.

Al reservar, el servicio consulta primero el repositorio JSON. Si el identificador
ya tiene contacto, utiliza automáticamente el correo y celular guardados; si no,
la interfaz solicita ambos valores y los guarda tras validar la reserva. El
correo es el canal principal. Si el proveedor de correo devuelve fallo o lanza
una excepción, `NotificadorReservas` intenta SMS/WhatsApp con el celular. Hasta
conectar proveedores reales, ambos canales registran una entrega simulada en
consola. Las funciones de integración están señaladas con comentarios `TODO` en
`notificador.py`; allí deben inyectarse tokens/credenciales de API, nunca datos
secretos de los usuarios.

La pestaña de usuarios también permite guardar ambos datos de contacto al
registrar el usuario. Al eliminar un usuario se elimina su contacto del JSON.
Las ejecuciones `--demo` y `--consola` no leen ni escriben contactos persistentes.

---

## Entidades del Dominio

1. **`Usuario`**: representa al estudiante inscrito en el gimnasio (nombre, número de documento y programa académico).
2. **`Reserva`**: representa el apartado de un cupo en un horario y fecha específicos (documento, nombre, horario, fecha, estado activo/cancelado). Cuenta con métodos para cancelar, confirmar/reactivar, comprobar titularidad y emitir resumen.
3. **`Visita`**: registra la asistencia física y el uso efectivo de las instalaciones (documento, horario, duración en minutos entre 1 y 90, fecha y lista de equipos utilizados).
4. **`Prioridad`**: representa un cupo exclusivo apartado preventivamente por un usuario de alta fidelidad (documento, nombre, horario, fecha, marca temporal de solicitud y estado de confirmación).
5. **`GymService`**: orquestador central que administra las colecciones mediante repositorios inyectados, valida las reglas de negocio, controla el límite de hasta 3 reservas activas semanales (`max_reservas_semana = 3`), gestiona el aforo máximo de 15 usuarios por franja y la agenda de turnos operativos (**08:00 AM a 08:00 PM**, cada 2 horas).

---

## Requisitos Funcionales Implementados (R1 a R15)

| ID | Operación / Método | Tipo | Descripción |
|:---:|---|:---:|---|
| **R1** | `registrar_usuario` | Tipo 1 | Registra un nuevo estudiante validando formato de texto y unicidad de documento. |
| **R2** | `eliminar_usuario` | Tipo 1 | Da de baja a un usuario validando coincidencia de nombre y documento, ejecutando la purga transaccional en cascada de sus reservas, visitas y prioridades *(Innovación Samuel Zapata)*. |
| **R3** | `realizar_reserva` | Tipo 1 | Aparta un cupo en una fecha y franja horaria válida. Controla el límite de una reserva activa diaria, máximo 3 reservas activas semanales por estudiante y el aforo máximo de 15 usuarios por franja. |
| **R4** | `registrar_visita` | Tipo 1 | Registra la asistencia efectiva, duración (1 a 90 min / 1:30 horas) y máquinas usadas. Fecha opcional (toma hoy por defecto) y previene visitas duplicadas en la misma franja y fecha. |
| **R5** | `horario_mas_frecuente` | Tipo 2 | Calcula la franja horaria con mayor afluencia de visitas. |
| **R6** | `programa_mas_frecuente` | Tipo 2 | Calcula la carrera universitaria con mayor número de estudiantes registrados. |
| **R7** | `cancelar_reserva` | Tipo 1 | Cambia el estado de una reserva activa a cancelada, liberando inmediatamente un cupo en la franja. |
| **R8** | `confirmar_reserva` | Tipo 1 | Reactiva una reserva previamente cancelada, validando aforo de 15, que el usuario no tenga otra reserva activa ese día ni supere las 3 reservas semanales *(Innovación Samuel Zapata)*. |
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

El sistema cuenta con una batería de **65 pruebas unitarias automatizadas** implementadas con la biblioteca estándar `unittest`:

```bash
python -m unittest test_gym.py test_contactos_notificaciones.py -v
```

### Cobertura por módulos:
- **`TestCapacidadPorFranja` (14 pruebas)**: Límite de aforo de 15 usuarios por franja, reserva número 16 rechazada con `CupoLlenoError`, liberación de cupos al cancelar, reactivación en franja llena, visitas como ocupantes, cómputo único por estudiante multirrol, visitante 16 rechazado, prevención de visitas duplicadas con `VisitaDuplicadaError`, visitas en diferentes franjas o fechas, visitas con fecha hoy por defecto, prioridad como cupo ocupado y desestimación de prioridad innecesaria para quien ya tiene reserva activa.
- **`TestPrioridades` (11 pruebas)**: Prioridad por usuario habitual (≥3 visitas), rechazo por incumplimiento de requisitos, reserva concurrente de franja con prioridad ajena, confirmación a tiempo, liberación automática por confirmación tardía, búsqueda inexistente, rechazo con menos de 2 horas de antelación, prioridad por mayor tiempo acumulado, bloqueo de reserva redundante al titular de la prioridad, reflejo de prioridad en disponibilidad y validación de datos vacíos.
- **`TestReservas` (7 pruebas)**: Reserva exitosa, rechazo por usuario no registrado, franja inválida, fecha inválida o año no bisiesto, doble reserva activa en el mismo día, ciclo completo de cancelación/reactivación y cancelación de reserva inexistente.
- **`TestUsuarios` (7 pruebas)**: Registro exitoso, duplicados rechazados, campos vacíos o solo espacios, saneamiento de espacios en documento, eliminación inexistente, eliminación con nombre incorrecto y eliminación en cascada atómica (usuarios, reservas, visitas y prioridades).
- **`TestVisitasYFechas` (6 pruebas)**: Registro exitoso de visita, duración inválida (cero, negativa o booleano), usuario no registrado, franja inválida, algoritmo matemático de años bisiestos y validador de calendario gregoriano.
- **`TestEstadisticas` (4 pruebas)**: Horario pico más frecuente, carrera académica más frecuente, promedio de duración en minutos por estudiante y comportamiento con repositorios vacíos.
- **`TestConsultasYDisponibilidad` (3 pruebas)**: Verificación de titularidad de reserva (Sí/No), resumen textual de reserva y consulta de estados de disponibilidad.
- **`TestEspaciosEnFechasYPrioridadesVigentes` (3 pruebas)**: Cancelación con espacios accidentales en la fecha, solicitud de prioridad con espacios y purga reactiva de prioridades vencidas.
- **`TestContactosJSON` y `TestNotificadorReservas` (7 pruebas)**: Persistencia exclusiva de los campos autorizados, recuperación automática del contacto, errores de lectura/escritura, eliminación del contacto y fallback correo/SMS.

---

## Equipo de Desarrollo

Proyecto desarrollado para la asignatura **Programación Orientada a Objetos** en la **Universidad de Medellín** (2026), docente **Mario Alejandro Saldarriaga Álvarez**.

- **Samuel Zapata Trujillo** — Módulo 1: Usuarios, Reservas, Aforo y Ensamblaje (`main.py`, `PanelUsuarios`, `PanelReservas`, R1, R2, R3, R7, R8).
- **Juan José Aguirre Durango** — Módulo 2: Visitas, Calendario y Estadísticas Analíticas (`PanelVisitas`, `PanelEstadisticas`, R4, R5, R6, R11, R15).
- **Angelina Negrette Diaz** — Módulo 3: Prioridades, Consultas y Diseño de Interfaz (`VentanaPrincipal`, `componentes.py`, `PanelPrioridades`, R9, R10, R12, R13, R14).
