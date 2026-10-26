python main.py --consola
```
---
## 🧪 Pruebas Unitarias Automatizadas
El sistema cuenta con una batería de **55 pruebas unitarias automatizadas** implementadas con la biblioteca estándar `unittest`:
```bash
python -m unittest test_gym.py -v
```
### Cobertura de las 55 Pruebas:
- **`TestCapacidadPorFranja` (14 pruebas)**: Límite de aforo de 15 usuarios por franja, reserva número 16 rechazada con `CupoLlenoError`, liberación de cupos al cancelar, reactivación en franja llena, visitas como ocupantes, cómputo único por estudiante multirrol, visitante 16 rechazado, prevención de visitas duplicadas con `VisitaDuplicadaError`, visitas en diferentes franjas o fechas, visitas con fecha hoy por defecto, prioridad como cupo ocupado y desestimación de prioridad innecesaria para quien ya tiene reserva activa.
- **`TestPrioridades` (11 pruebas)**: Prioridad por usuario habitual (≥3 visitas), rechazo por incumplimiento de requisitos, reserva concurrente de franja con prioridad ajena, confirmación a tiempo, liberación automática por confirmación tardía, búsqueda inexistente, rechazo con menos de 2 horas de antelación, prioridad por mayor tiempo acumulado, bloqueo de reserva redundante al titular de la prioridad, reflejo de prioridad en disponibilidad y validación de datos vacíos.
- **`TestReservas` (7 pruebas)**: Reserva exitosa, rechazo por usuario no registrado, franja inválida, fecha inválida o año no bisiesto, doble reserva activa en el mismo día, ciclo completo de cancelación/reactivación y cancelación de reserva inexistente.
- **`TestUsuarios` (7 pruebas)**: Registro exitoso, duplicados rechazados, campos vacíos o solo espacios, saneamiento de espacios en documento, eliminación inexistente, eliminación con nombre incorrecto y eliminación en cascada atómica (usuarios, reservas, visitas y prioridades).
- **`TestVisitasYFechas` (6 pruebas)**: Registro exitoso de visita, duración inválida (cero, negativa o booleano), usuario no registrado, franja inválida, algoritmo matemático de años bisiestos y validador de calendario gregoriano.
- **`TestEstadisticas` (4 pruebas)**: Horario pico más frecuente, carrera académica más frecuente, promedio de duración en minutos por estudiante y comportamiento con repositorios vacíos.
- **`TestConsultasYDisponibilidad` (3 pruebas)**: Verificación de titularidad de reserva (Sí/No), resumen textual de reserva y consulta de estados de disponibilidad.
- **`TestEspaciosEnFechasYPrioridadesVigentes` (3 pruebas)**: Cancelación con espacios accidentales en la fecha, solicitud de prioridad con espacios y purga reactiva de prioridades vencidas.
---
## 👥 Equipo de Desarrollo
Proyecto desarrollado para la asignatura **Programación Orientada a Objetos** en la **Universidad de Medellín** (2026), bajo la tutoría del docente **Mario Alejandro Saldarriaga Álvarez**.
- **Samuel Zapata Trujillo** — Módulo 1: Usuarios, Reservas, Aforo y Ensamblaje (`main.py`, `PanelUsuarios`, `PanelReservas`, R1, R2, R3, R7, R8).
- **Juan José Aguirre Durango** — Módulo 2: Visitas, Calendario y Estadísticas Analíticas (`PanelVisitas`, `PanelEstadisticas`, R4, R5, R6, R11, R15).
- **Angelina Negrette Diaz** — Módulo 3: Prioridades, Consultas y Diseño de Interfaz (`VentanaPrincipal`, `componentes.py`, `PanelPrioridades`, R9, R10, R12, R13, R14).
