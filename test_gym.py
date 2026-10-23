class TestReservas(unittest.TestCase):
    """Pruebas de HU-02 (Samuel): R3, R7 y R8."""

    def setUp(self):
        self.gym = crear_gym()
        self.gym.registrar_usuario("Mariana Restrepo", "1004", "Administración")

    def test_reserva_exitosa_informa_tiempo_maximo(self):
        mensaje = self.gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        self.assertIn("¡Reserva exitosa! Mariana Restrepo tiene su espacio a las 08:00 AM.", mensaje)
        self.assertIn("1:30 horas", mensaje)

    def test_usuario_no_registrado(self):
        with self.assertRaises(UsuarioNoRegistradoError):
            self.gym.realizar_reserva("999", "08:00 AM", FECHA, AHORA)

    def test_fechas_invalidas(self):
        for fecha in ("2025-02-29", "2025/06/15", "2025-13-01", ""):
            with self.subTest(fecha=fecha):
                with self.assertRaises(FechaInvalidaError):
                    self.gym.realizar_reserva("1004", "08:00 AM", fecha, AHORA)

    def test_horario_invalido_informa_horarios_disponibles(self):
        with self.assertRaises(HorarioInvalidoError) as contexto:
            self.gym.realizar_reserva("1004", "09:00 AM", FECHA, AHORA)
        self.assertIn("08:00 AM | 10:00 AM | 02:00 PM", str(contexto.exception))

    def test_una_sola_reserva_activa_por_fecha(self):
        self.gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        with self.assertRaises(ReservaDuplicadaError):
            self.gym.realizar_reserva("1004", "10:00 AM", FECHA, AHORA)
        self.gym.realizar_reserva("1004", "10:00 AM", "2025-06-16", AHORA)

    def test_cancelar_y_cancelar_otra_vez(self):
        self.gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        self.assertEqual(self.gym.cancelar_reserva("1004", "08:00 AM", FECHA),
                         "Reserva de Mariana Restrepo a las 08:00 AM cancelada.")
        self.assertIn("ya estaba cancelada",
                      self.gym.cancelar_reserva("1004", "08:00 AM", FECHA))
        self.assertFalse(self.gym.listar_reservas()[0].activa)

    def test_cancelar_o_confirmar_reserva_inexistente(self):
        with self.assertRaises(ReservaNoEncontradaError):
            self.gym.cancelar_reserva("1004", "08:00 AM", FECHA)
        with self.assertRaises(ReservaNoEncontradaError):
            self.gym.confirmar_reserva("1004", "08:00 AM", FECHA, AHORA)

    def test_confirmar_reactiva_y_confirmar_activa_no_cambia(self):
        self.gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        self.gym.cancelar_reserva("1004", "08:00 AM", FECHA)
        self.assertEqual(self.gym.confirmar_reserva("1004", "08:00 AM", FECHA, AHORA),
                         "Reserva de Mariana Restrepo confirmada nuevamente para las 08:00 AM.")
        self.assertIn("ya está activa",
                      self.gym.confirmar_reserva("1004", "08:00 AM", FECHA, AHORA))

    def test_cancelada_y_vuelta_a_crear_cancelar_actua_sobre_la_activa(self):
        self.gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        self.gym.cancelar_reserva("1004", "08:00 AM", FECHA)
        self.gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)  # nueva activa
        mensaje = self.gym.cancelar_reserva("1004", "08:00 AM", FECHA)
        self.assertNotIn("ya estaba cancelada", mensaje)
        self.assertTrue(all(not r.activa for r in self.gym.listar_reservas()))

    def test_reactivar_respeta_una_reserva_activa_por_fecha(self):
        self.gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        self.gym.cancelar_reserva("1004", "08:00 AM", FECHA)
        self.gym.realizar_reserva("1004", "10:00 AM", FECHA, AHORA)
        with self.assertRaises(ReservaDuplicadaError):
            self.gym.confirmar_reserva("1004", "08:00 AM", FECHA, AHORA)

    def test_cupo_apartado_por_otro_usuario(self):
        prioridad = SimpleNamespace(documento="2", nombre="Luis",
                                    horario="08:00 AM", fecha=FECHA)
        gym = crear_gym(prioridades=RepoFalso([prioridad]))
        gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(CupoApartadoError):
            gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        gym.realizar_reserva("1004", "10:00 AM", FECHA, AHORA)  # otro horario sí
        gym.cancelar_reserva("1004", "10:00 AM", FECHA)

    def test_cupo_propio_con_prioridad_no_necesita_reserva(self):
        prioridad = SimpleNamespace(documento="1004", nombre="Mariana",
                                    horario="08:00 AM", fecha=FECHA)
        gym = crear_gym(prioridades=RepoFalso([prioridad]))
        gym.registrar_usuario("Mariana", "1004", "Administración")
        with self.assertRaises(ReservaDuplicadaError):
            gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)

    def test_reactivar_respeta_cupo_exclusivo_de_otro(self):
        prioridades = RepoFalso()
        gym = crear_gym(prioridades=prioridades)
        gym.registrar_usuario("Mariana", "1004", "Administración")
        gym.realizar_reserva("1004", "08:00 AM", FECHA, AHORA)
        gym.cancelar_reserva("1004", "08:00 AM", FECHA)
        prioridades.elementos.append(SimpleNamespace(
            documento="2", nombre="Luis", horario="08:00 AM", fecha=FECHA))
        with self.assertRaises(CupoApartadoError):
            gym.confirmar_reserva("1004", "08:00 AM", FECHA, AHORA)

    def test_todos_los_errores_heredan_de_gymerror(self):
        with self.assertRaises(GymError):
            self.gym.realizar_reserva("999", "08:00 AM", FECHA, AHORA)
