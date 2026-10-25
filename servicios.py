def registrar_visita(self, documento: str, horario: str, duracion: int, equipos: list[str]) -> str:
        doc_limpio = str(documento).strip()
        usuario = self._exigir_usuario(doc_limpio)
        self._validar_horario(horario)