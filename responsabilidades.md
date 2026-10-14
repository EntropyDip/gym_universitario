# Historias de Usuario y Plan de Trabajo (Entrega 2) – Gimnasio universitario

Oct 14, 2026 · @Samuel

El trabajo se reparte en tres módulos de 18 puntos de esfuerzo cada uno (33,3 % por integrante), con ramas por historia de usuario, revisión cruzada de cada pull request y una sustentación preparada desde el primer día.

**Proyecto:** Sistema de gestión de gimnasio universitario

**Asignatura:** Programación Orientada a Objetos · **Institución:** Universidad de Medellín

**Docente:** Mario Alejandro Saldarriaga Álvarez

**Equipo:** Juan José Aguirre Durango, Angelina Negrette Diaz, Samuel Zapata Trujillo

**Repositorio:** https://github.com/EntropyDip/gym\_universitario.git

## 1. Lineamientos técnicos de la Entrega 2

La entrega pide diseño e implementación completa, manejo de excepciones, interfaz gráfica y buena modularización. Estas reglas son obligatorias para los tres.

- **Arquitectura por capas.** `modelos.py` (entidades y validación de sus datos) → `repositorios.py` (almacenamiento: clase abstracta y versión en memoria) → `servicios.py` (reglas de negocio en `GymService`) → `interfaz/` (solo presentación).
- **La interfaz no contiene reglas de negocio.** Llama a los métodos del servicio y a `listar_*`; nunca toca las listas internas.
- **Excepciones, no textos de error.** Toda regla violada lanza una excepción que hereda de `GymError`. La interfaz la captura y la muestra en un cuadro de diálogo. Prohibido `print` en modelos y servicios.
- **Hora inyectable.** Los métodos que dependen del tiempo reciben `hora_actual` como parámetro opcional (por defecto, el reloj del sistema), para poder probarlos.
- **Nombres del documento de análisis.** Atributos y métodos usan exactamente los nombres de las secciones 2.4, 3.1 y 3.2 del documento. Si uno cambia en el código, se cambia el mismo día en el documento.
- **Estilo.** `snake_case` en funciones y atributos, `PascalCase` en clases, docstring en cada clase y método público.
- **Librerías externas.** `matplotlib` y `tkcalendar`, declaradas en `requirements.txt`.
- **Participación.** Los tres programan y todo el código debe poder sustentarlo cualquiera de los tres.
- **Sin código muerto.** `proyecto_gym.py` se elimina con `git rm` cuando su lógica ya esté migrada.

## 2. Matriz de distribución equitativa del trabajo

Son 15 requisitos funcionales, 5 por integrante. Cada uno también construye las pantallas de sus requisitos y las pruebas de su parte. Los puntos son una estimación de esfuerzo del equipo y suman 18 por persona.

| Integrante | Módulo | Requisitos | Clases y componentes clave | Puntos |
| --- | --- | --- | --- | --- |
| Samuel Zapata Trujillo | Módulo 1: Usuarios, Reservas y ensamblaje | R1, R2, R3, R7, R8 | Usuario, Reserva, UsuarioRepositorio, ReservaRepositorio, PanelUsuarios, PanelReservas, main.py | 18 |
| Juan José Aguirre Durango | Módulo 2: Visitas y Estadísticas | R4, R5, R6, R11, R15 | es\_bisiesto, es\_fecha\_valida, Visita, VisitaRepositorio, PanelVisitas, PanelEstadisticas | 18 |
| Angelina Negrette Diaz | Módulo 3: Prioridades, Consultas de reserva y Diseño | R9, R10, R12, R13, R14 | Prioridad, PrioridadRepositorio, VentanaPrincipal, componentes, PanelPrioridades, diagrama de clases v2 | 18 |

**Compartido.** `excepciones.py` (cada uno agrega las excepciones de sus reglas), `test_gym.py` (cada uno escribe la clase de pruebas de su módulo) y el `README.md`.

**Integración entre módulos.** El panel de reservas de Samuel muestra la disponibilidad (R14) y los botones de R9 y R10, que usan métodos de Angelina. La prioridad de Angelina usa las visitas de Juan José. Por eso la sección 5 fija el orden de integración.

## 3. Metodología de trabajo en Git

### 3.1 Una rama por historia de usuario

Nadie hace commits directos en `main`. Cada historia se trabaja en su propia rama, creada desde `main` actualizado.

| Rama | Responsable |
| --- | --- |
| feature/HU-01-usuarios | Samuel |
| feature/HU-02-reservas | Samuel |
| feature/HU-03-interfaz-ensamblaje | Samuel |
| feature/HU-04-visitas | Juan José |
| feature/HU-05-estadisticas | Juan José |
| feature/HU-06-interfaz-visitas-estadisticas | Juan José |
| feature/HU-07-consultas-reserva | Angelina |
| feature/HU-08-prioridades | Angelina |
| feature/HU-09-interfaz-diseno | Angelina |

### 3.2 Commits pequeños y prueba previa

- Un commit por método, clase o regla terminada, no uno gigante al final.
- Formato `tipo(ámbito): descripción` con los tipos `feat`, `fix`, `test`, `docs` y `refactor`. Ejemplos: `feat(reservas): validar una sola reserva activa por fecha`, `fix(prioridades): liberar cupo si pasaron 2 horas`, `test(visitas): rechazar duración cero`.
- Antes de cada commit se ejecuta `python -m unittest` y `python main.py --consola`. Si algo falla, no se hace commit.
- Así, ante una regresión se identifica el commit responsable y se revierte sin perder el resto.

### 3.3 Pull request con descripción completa

Al terminar los criterios de aceptación de la historia, se hace `git push origin <rama>` y se abre un pull request hacia `main`. La descripción incluye:

- Qué historia de usuario y qué requisitos atiende.
- Qué clases, métodos y excepciones se agregaron o modificaron.
- Qué pruebas se ejecutaron y su resultado (salida de `python -m unittest`).
- Una captura de pantalla, si la historia toca la interfaz.

### 3.4 Revisión cruzada obligatoria

Nadie fusiona su propio pull request. La revisión rota para que los tres conozcan todo el código, lo que ayuda en la sustentación:

| Autor del PR | Lo revisa y fusiona |
| --- | --- |
| Samuel | Angelina |
| Juan José | Samuel |
| Angelina | Juan José |

El revisor verifica que:

- Los nombres coinciden con el documento de análisis y con los demódulos.
- Cada regla violada lanza la excepción correcta de `excepciones.py`.
- No hay lógica de negocio en la interfaz.
- Las pruebas pasan y cubren los criterios de aceptación.
- Hay docstrings y los commits son atómicos y claros.

### 3.5 Definición de terminado

Una historia está terminada cuando:

- [ ] Cumple todos sus criterios de aceptación.
- [ ] Tiene pruebas unitarias que pasan.
- [ ] Su PR fue revisado y fusionado por otra persona.
- [ ] El documento de análisis sigue coincidiendo con el código.
- [ ] Quien la hizo puede explicarla sin mirar el código.

## 4. Historias de usuario y listas de tareas

### Responsable 1: Samuel Zapata Trujillo

**Módulo:** Usuarios, Reservas y ensamblaje

**HU-01: Registro y eliminación de usuarios** (5 puntos)

- **Como:** administrador del gimnasio.
- **Quiero:** registrar usuarios con sus datos académicos y eliminarlos junto con todo lo que les pertenece.
- **Para:** tener un registro único y limpio de quiénes usan el gimnasio.
- **Requisitos:** R1, R2.

Criterios de aceptación:

- Registrar un documento ya existente lanza `UsuarioYaRegistradoError` y no modifica nada.
- Un nombre, documento o programa vacío lanza `DatoVacioError`.
- Eliminar con nombre y documento que no coinciden lanza `UsuarioNoRegistradoError`.
- Al eliminar un usuario se eliminan también sus reservas, visitas y prioridades.

Lista de tareas:

- [ ] Clase `Usuario` con validación en `__post_init__`.
- [ ] `UsuarioRepositorio` (abstracto) y `UsuarioRepositorioMemoria`.
- [ ] `registrar_usuario` y `eliminar_usuario` en `GymService`.
- [ ] Pruebas: duplicado, vacíos, nombre que no coincide y eliminación en cascada.

*Guía:* el documento se guarda sin espacios sobrantes (`strip`) para que `1004` y ` 1004  ` no cuenten como usuarios distintos.

**HU-02: Reservas de cupos** (8 puntos)

- **Como:** usuario del gimnasio.
- **Quiero:** reservar, cancelar y reactivar un cupo por fecha y horario.
- **Para:** planear mi rutina sin enviar correos.
- **Requisitos:** R3, R7, R8.

Criterios de aceptación:

- Una reserva válida responde con el mensaje de éxito y el tiempo máximo de la sesión.
- Un usuario no puede tener dos reservas activas en la misma fecha (`ReservaDuplicadaError`).
- Un horario fuera de la lista lanza `HorarioInvalidoError`; una fecha inválida, `FechaInvalidaError`.
- Un cupo apartado con prioridad por otro usuario lanza `CupoApartadoError`.
- Cancelar o confirmar una reserva que ya está en ese estado no cambia nada y lo informa.
- Si existe una reserva cancelada y otra activa con los mismos datos, cancelar actúa sobre la activa.
- Reactivar una reserva respeta la regla de una reserva activa por fecha y el cupo exclusivo.

Lista de tareas:

- [ ] Clase `Reserva` con `cancelar()`, `confirmar()`, `coincide_con()` y `mostrar_resumen()`.
- [ ] `ReservaRepositorio` y `ReservaRepositorioMemoria` (incluye `buscar` y `eliminar_por_documento`).
- [ ] `realizar_reserva`, `cancelar_reserva` y `confirmar_reserva`.
- [ ] Pruebas de cada criterio, incluida la reserva cancelada y vuelta a crear.

*Guía:* el orden de las validaciones de `realizar_reserva` es: usuario, fecha, liberar prioridades vencidas, horario, prioridad de otro, reserva activa. Así coincide con la sección 3.1 del documento.

**HU-03: Interfaz de usuarios y reservas, y ensamblaje** (5 puntos)

- **Como:** administrador y usuario.
- **Quiero:** una ventana donde registrar usuarios y manejar reservas, y un punto de entrada que arme todo.
- **Para:** usar el sistema sin conocer el código.
- **Requisitos:** R1, R2, R3, R7, R8 (pantallas P1 y P2).

Criterios de aceptación:

- `PanelUsuarios` registra y elimina (con confirmación) y muestra la tabla de usuarios.
- `PanelReservas` reserva, cancela y confirma, y muestra las reservas registradas.
- Todo error se muestra en un cuadro de diálogo y la aplicación no se cierra.
- `python main.py` abre la interfaz, `--demo` carga datos de ejemplo y `--consola` corre el flujo de punta a punta.

Lista de tareas:

- [ ] `PanelUsuarios` y `PanelReservas` usando `PanelBase.ejecutar`.
- [ ] `main.py`: `crear_servicio`, `cargar_datos_demo` y `flujo_consola` con `try/except GymError`.
- [ ] Integrar los paneles de los otros dos módulos cuando estén fusionados.
- [ ] `README.md` con instrucciones de ejecución.

*Guía:* el panel nunca valida reglas; solo lee los campos, llama al servicio y muestra el mensaje o el error.

### Responsable 2: Juan José Aguirre Durango

**Módulo:** Visitas y Estadísticas

**HU-04: Registro de visitas y validación de fechas** (5 puntos)

- **Como:** encargado del gimnasio.
- **Quiero:** registrar cada visita con su horario, duración y equipos usados.
- **Para:** tener datos reales de afluencia en lugar de correos dispersos.
- **Requisitos:** R4.

Criterios de aceptación:

- `es_fecha_valida` acepta `2024-02-29` y rechaza `2025-02-29`, `2025/06/15` y `2025-13-01`.
- Una duración menor o igual a 0, o no entera, lanza `DuracionInvalidaError`.
- Un documento no registrado lanza `UsuarioNoRegistradoError`; un horario inválido, `HorarioInvalidoError`.
- La lista de equipos se guarda sin textos vacíos ni espacios sobrantes.

Lista de tareas:

- [ ] `es_bisiesto` y `es_fecha_valida` en `modelos.py`.
- [ ] Clase `Visita` con validación en `__post_init__`.
- [ ] `VisitaRepositorio` y `VisitaRepositorioMemoria`.
- [ ] `registrar_visita` en `GymService` y sus pruebas.

*Guía:* `True` y `False` son enteros en Python; la validación de duración debe excluirlos explícitamente.

**HU-05: Estadísticas de uso** (8 puntos)

- **Como:** encargado del gimnasio.
- **Quiero:** conocer horarios pico, programas más frecuentes, tiempo promedio y equipos más usados.
- **Para:** tomar decisiones sobre el espacio y el desgaste de las máquinas.
- **Requisitos:** R5, R6, R11, R15.

Criterios de aceptación:

- `horario_mas_frecuente` y `programa_mas_frecuente` devuelven el valor con más apariciones, o un aviso si no hay datos.
- `promedio_duracion_por_usuario` muestra el promedio en minutos con un decimal, por usuario.
- `equipo_mas_utilizado` ordena los equipos de mayor a menor y cuenta una vez por visita, sin distinguir mayúsculas.
- Los datos para los gráficos salen de `datos_promedio_duracion` y `ranking_equipos`.

Lista de tareas:

- [ ] Los cuatro métodos de estadística en `GymService`.
- [ ] Los dos métodos de datos que usan los gráficos.
- [ ] Pruebas con datos conocidos y con el sistema vacío.

*Guía:* verifica a mano un promedio (por ejemplo 40 y 60 minutos dan 50,0) antes de escribir la prueba.

**HU-06: Interfaz de visitas y estadísticas** (5 puntos)

- **Como:** encargado del gimnasio.
- **Quiero:** registrar visitas desde una pantalla y ver las estadísticas con gráficos.
- **Para:** consultar la información de un vistazo.
- **Requisitos:** R4, R5, R6, R11, R15 (pantallas P3 y P5).

Criterios de aceptación:

- `PanelVisitas` permite elegir equipos de una lista o escribir otros, y muestra la tabla de visitas.
- `PanelEstadisticas` muestra el horario y el programa más frecuentes y dos gráficos de barras con `matplotlib`.
- Un campo de duración que no es número muestra un mensaje claro.
- Sin datos, los gráficos muestran «Sin datos» y no fallan.

Lista de tareas:

- [ ] `PanelVisitas` y `PanelEstadisticas`.
- [ ] `requirements.txt` con las librerías externas.
- [ ] Probar la pantalla con `python main.py --demo`.

*Guía:* si `matplotlib` no está instalado, el panel debe mostrar un texto y no romper la aplicación.

### Responsable 3: Angelina Negrette Diaz

**Módulo:** Prioridades, Consultas de reserva y Diseño

**HU-07: Consultas de reserva y disponibilidad** (5 puntos)

- **Como:** usuario del gimnasio.
- **Quiero:** ver si tengo reserva, su resumen y qué horarios están libres en una fecha.
- **Para:** no escribir mensajes a ciegas cuando la franja ya está ocupada.
- **Requisitos:** R9, R10, R14.

Criterios de aceptación:

- `verificar_propietario_reserva` devuelve «Sí» si hay al menos una reserva del documento y «No» si no.
- `mostrar_resumen_reserva` muestra usuario, documento, fecha, horario y estado de la reserva más reciente; si no existe, lanza `ReservaNoEncontradaError`.
- `consultar_disponibilidad` devuelve, para cada horario, si está libre, reservado o apartado con prioridad (y por quién).
- Una fecha inválida lanza `FechaInvalidaError`.

Lista de tareas:

- [ ] Los tres métodos en `GymService`.
- [ ] Pruebas de los tres estados de disponibilidad.
- [ ] Entregar a Samuel el formato de lo que devuelve R14 para su tabla.

*Guía:* libera las prioridades vencidas antes de calcular la disponibilidad, o un cupo caducado aparecerá como apartado.

**HU-08: Prioridad de membresía** (8 puntos)

- **Como:** usuario habitual del gimnasio.
- **Quiero:** apartar un cupo con exclusividad y confirmar mi asistencia a tiempo.
- **Para:** tener garantizado mi horario de siempre.
- **Requisitos:** R12, R13.

Criterios de aceptación:

- Es habitual quien tiene 3 o más visitas en ese horario, o quien acumula estrictamente más minutos que todos los demás; un empate no cuenta.
- Quien no cumple lanza `PrioridadNoCumpleError`; un cupo ya apartado, `CupoApartadoError`.
- No se puede pedir prioridad si faltan menos de 2 horas para el horario.
- Confirmar con 2 horas o más de antelación deja el cupo exclusivo; después de ese límite la prioridad se elimina y el cupo se libera.
- Una prioridad que no existe lanza `PrioridadNoEncontradaError`.
- Una prioridad confirmada no vence.

Lista de tareas:

- [ ] Clase `Prioridad` con `limite_confirmacion()`, `esta_vencida()` y `confirmar()`.
- [ ] `PrioridadRepositorio` y `PrioridadRepositorioMemoria`.
- [ ] `prioridad_membresia`, `confirmar_prioridad` y `_liberar_prioridades_vencidas`.
- [ ] Pruebas con horas fijas: justo en el límite, un minuto después, empate de tiempo.

*Guía:* usa siempre una `hora_actual` fija en las pruebas. El límite exacto (2 horas antes) todavía se acepta; un minuto después ya no.

**HU-09: Ventana principal, prioridades y diseño** (5 puntos)

- **Como:** usuario del sistema.
- **Quiero:** una ventana con pestañas, una pantalla para prioridades y un diseño documentado.
- **Para:** navegar el sistema fácilmente y que el diseño sea claro.
- **Requisitos:** R12, R13 (pantalla P4) y el diagrama de clases.

Criterios de aceptación:

- `VentanaPrincipal` agrega una pestaña por panel y los refresca al cambiar de pestaña.
- `PanelPrioridades` solicita y confirma prioridad y muestra la lista con su límite de confirmación y su estado.
- `componentes.py` ofrece la base de los paneles, las tablas y los selectores de fecha y horario.
- El diagrama de clases v2 muestra `GymService`, los repositorios, las excepciones y los paneles, y su enlace está en el documento.

Lista de tareas:

- [ ] `VentanaPrincipal`, `componentes.py` y `PanelPrioridades`.
- [ ] Dibujar el diagrama de clases v2 y actualizar el enlace.
- [ ] Revisar que las secciones 3.1 a 3.5 del documento coincidan con el código.

*Guía:* el selector de fecha usa `tkcalendar` si está instalado y un campo de texto AAAA-MM-DD si no.

## 5. Dependencias y orden de integración

| Historia | Depende de |
| --- | --- |
| HU-01 y HU-04 | Nada; se hacen primero, en paralelo |
| HU-02 | HU-01 (necesita Usuario) |
| HU-05 | HU-01 y HU-04 (usuarios y visitas) |
| HU-08 | HU-01 y HU-04 (Usuario y Visita para saber si es habitual) |
| HU-07 | HU-02 y HU-08 (reservas y prioridades) |
| HU-03, HU-06, HU-09 | Los métodos de servicio que cada pantalla invoca |

Orden de fusión a `main`: primero HU-01 y HU-04; después HU-02, HU-05 y HU-08; luego HU-07; al final las tres historias de interfaz.

## 6. Plan de integración y validación conjunta

Cuando los módulos estén fusionados, los tres se reúnen y recorren esta lista con `python main.py --consola` y después con la interfaz (`python main.py --demo`):

- [ ] **Paso 1 (Samuel y Juan José):** registrar dos usuarios, registrar visitas y verificar que una duración de 0 lance el error esperado.
- [ ] **Paso 2 (Samuel):** reservar un horario, intentar una segunda reserva el mismo día y comprobar el error.
- [ ] **Paso 3 (Juan José y Angelina):** con tres visitas en un horario, solicitar prioridad y confirmarla.
- [ ] **Paso 4 (Angelina y Samuel):** intentar reservar el cupo apartado con otro usuario y comprobar `CupoApartadoError`.
- [ ] **Paso 5 (Angelina):** confirmar una prioridad pasado el límite y verificar que el cupo queda libre.
- [ ] **Paso 6 (Juan José):** revisar horario más frecuente, promedio por usuario y ranking de equipos.
- [ ] **Paso 7 (los tres):** eliminar un usuario y comprobar que desaparecen sus reservas, visitas y prioridades.
- [ ] **Paso 8 (los tres):** abrir cada pantalla, provocar un error y verificar que aparece el cuadro de diálogo sin cerrar la aplicación.

## 7. Plan de sustentación

En la primera entrega la sustentación fue la nota más baja, y todo el código debe poder sustentarlo cualquier integrante. Por eso la revisión cruzada y este plan son obligatorios.

| Integrante | Debe poder explicar | Preguntas probables |
| --- | --- | --- |
| Samuel | El flujo completo de `realizar_reserva`, el repositorio y el ensamblaje en `main.py` | ¿Por qué la validación va en el servicio y no en la interfaz? ¿Qué pasa si cancelo y vuelvo a reservar el mismo horario? |
| Juan José | Las estadísticas, la validación de fechas y bisiestos, y los gráficos | ¿Cómo se calcula el promedio por usuario? ¿Por qué 2100 no es bisiesto? |
| Angelina | `prioridad_membresia`, `confirmar_prioridad` y el vencimiento automático | ¿Qué pasa si dos usuarios empatan en minutos? ¿Cómo se calcula el límite de 2 horas? |

Reglas del equipo:

- Cada integrante también explica, a grandes rasgos, el módulo de los otros dos.
- Los tres saben explicar por qué se separan modelos, repositorios, servicios e interfaz.
- Se hace un ensayo completo antes de la entrega, con preguntas cruzadas.

## 8. Mapa de criterios de calificación

La tabla enlaza lo que pide la entrega con lo que lo cubre en este plan.

| Lo que se evalúa | Cómo se cubre | Responsable |
| --- | --- | --- |
| Descomposición de todos los requisitos | Sección 3.1 del documento, R1 a R15, con subtareas | Angelina (HU-09) |
| Diagrama de clases, versión nueva | Diagrama v2 con servicio, repositorios, excepciones y paneles | Angelina (HU-09) |
| Implementación de todos los requisitos con excepciones | `GymService` y excepciones de `excepciones.py` | Los tres (HU-01, 02, 04, 05, 07, 08) |
| Interfaz gráfica | Paneles P1 a P5 y ventana principal | Los tres (HU-03, 06, 09) |
| Modularización y organización | Capas: modelos, repositorios, servicios, interfaz | Los tres, verificado en la revisión cruzada |
| Repositorio con participación de todos | Ramas por historia, commits atómicos y PR revisados | Los tres |
| Sustentación | Sección 7 | Los tres |
