# Sistema de Gestión de Gimnasio Universitario

Sistema en Python para administrar usuarios, reservas y visitas de un gimnasio universitario. Permite registrar usuarios, gestionar reservas de horarios, llevar un control de visitas con los equipos utilizados, y obtener estadísticas sobre los horarios y programas académicos más frecuentes.

## Descripción

El proyecto modela el mundo de un gimnasio a través de 5 entidades:

- **`Usuario`**: representa a un estudiante inscrito en el gimnasio (nombre, documento y programa académico).
- **`Reserva`**: representa el apartado de un horario por parte de un usuario, con su propio comportamiento (cancelar, confirmar, verificar propietario, mostrar resumen).
- **`Visita`**: registra que un usuario asistió al gimnasio en un horario dado, con la duración de la visita y los equipos usados.
- **`Prioridad`**: representa un cupo apartado con prioridad para un usuario en un horario y fecha específicos, con estado de confirmación.
- **`Gym`**: entidad central que administra la colección de usuarios, reservas, visitas y prioridades, y gestiona los horarios disponibles.

## Funcionalidades

| Función | Descripción |
|---|---|
| `registrar_usuario` | Registra un nuevo usuario validando que el documento no esté duplicado. |
| `eliminar_usuario` | Elimina un usuario existente por nombre y documento, junto con sus reservas, visitas y prioridades asociadas. |
| `realizar_reserva` | Crea una reserva validando que el usuario exista, no tenga ya una reserva activa ese día, que el horario solicitado sea válido y que no esté apartado con prioridad por otro usuario. |
| `registrar_visita` | Registra una visita (horario, duración y equipos usados) de un usuario ya registrado. |
| `horario_mas_frecuente` | Calcula el horario con mayor cantidad de visitas registradas. |
| `programa_mas_frecuente` | Calcula el programa académico con más usuarios registrados. |
| `Reserva.cancelar` | Cambia el estado de una reserva activa a cancelada. |
| `Reserva.confirmar` | Reactiva una reserva previamente cancelada. |
| `Reserva.coincide_con` | Verifica si una reserva pertenece a un documento dado. |
| `Reserva.mostrar_resumen` | Genera un resumen textual del estado de la reserva. |
| `promedio_duracion_por_usuario` | Calcula para cada usuario el promedio de duración de sus visitas registradas. |
| `prioridad_membresia` | Otorga prioridad a un usuario para reservar un horario si es "habitual" (≥3 visitas) o tiene mayor tiempo acumulado. |
| `confirmar_prioridad` | Confirma una prioridad antes del límite de 2 horas; de lo contrario, el cupo se libera. |

## Restricciones

- No se permiten **documentos duplicados** al registrar un usuario.
- Un usuario solo puede tener **una reserva activa por fecha**.
- El horario solicitado debe pertenecer a la lista de `horarios_disponibles` del gimnasio.
- Las visitas y reservas solo pueden registrarse a nombre de usuarios **ya registrados**.
- Cancelar/confirmar una reserva no tiene efecto si ya se encuentra en ese estado (evita transiciones redundantes).
- Los datos de creación de usuarios, reservas y prioridades no pueden estar vacíos (el sistema levanta un `ValueError`).
- Las fechas deben ingresarse en formato estricto `AAAA-MM-DD` y el sistema valida matemáticamente que existan en el calendario (incluyendo años bisiestos).
- La prioridad sobre un horario se otorga si el usuario es "habitual" en ese horario (≥3 visitas registradas a esa hora, **sin importar la fecha en que ocurrieron esas visitas**) o si acumula estrictamente más minutos de uso que cualquier otro usuario; en caso de empate en el tiempo acumulado, ningún usuario obtiene prioridad por ese criterio.
- Un horario con prioridad otorgada queda reservado exclusivamente para ese usuario: nadie más puede reservarlo ni pedir prioridad sobre él mientras la prioridad siga vigente.
- Una prioridad no confirmada dentro de las 2 horas previas al horario se libera automáticamente, ya sea al intentar confirmarla, al intentar reservar ese horario, o al pedir una nueva prioridad.
- Eliminar un usuario también elimina sus reservas, visitas y prioridades asociadas.

