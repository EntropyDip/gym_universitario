# Sistema de Gestión de Gimnasio Universitario

Sistema en Python para administrar usuarios, reservas y visitas de un gimnasio universitario. Permite registrar usuarios, gestionar reservas de horarios, llevar un control de visitas con los equipos utilizados, y obtener estadísticas sobre los horarios y programas académicos más frecuentes.

## Descripción

El proyecto modela el mundo de un gimnasio a través de tres entidades principales:

- **`Usuario`**: representa a un estudiante inscrito en el gimnasio (nombre, documento y programa académico).
- **`Reserva`**: representa el apartado de un horario por parte de un usuario, con su propio comportamiento (cancelar, confirmar, verificar propietario, mostrar resumen).
- **`Gym`**: entidad central que administra la colección de usuarios y reservas, gestiona los horarios disponibles y lleva el registro de visitas.

## Funcionalidades

| Función | Descripción |
|---|---|
| `registrar_usuario` | Registra un nuevo usuario validando que el documento no esté duplicado. |
| `eliminar_usuario` | Elimina un usuario existente por nombre y documento. |
| `realizar_reserva` | Crea una reserva validando que el usuario exista, no tenga ya una reserva activa ese día, y que el horario solicitado sea válido. |
| `registrar_visita` | Registra una visita (horario, duración y equipos usados) de un usuario ya registrado. |
| `horario_mas_frecuente` | Calcula el horario con mayor cantidad de visitas registradas. |
| `programa_mas_frecuente` | Calcula el programa académico con más usuarios registrados. |
| `Reserva.cancelar` | Cambia el estado de una reserva activa a cancelada. |
| `Reserva.confirmar` | Reactiva una reserva previamente cancelada. |
| `Reserva.coincide_con` | Verifica si una reserva pertenece a un documento dado. |
| `Reserva.mostrar_resumen` | Genera un resumen textual del estado de la reserva. |
