class DirectorDificultad:
    """Controla el ritmo de aparición y la escala de enemigos por tiempo."""

    DURACION_NIVEL = 30.0
    PRIMER_ELITE = 60.0

    def __init__(self):
        self.proximo_elite = self.PRIMER_ELITE

    def nivel(self, tiempo_supervivencia):
        return int(tiempo_supervivencia // self.DURACION_NIVEL)

    def intervalo_mariposa(self, nivel):
        return max(0.35, 1.0 * (0.93 ** nivel))

    def intervalo_fantasma(self, nivel):
        return max(0.90, 3.0 * (0.95 ** nivel))

    def maximo_enemigos(self, nivel):
        return min(90, 50 + nivel * 4)

    def puede_generar(self, cantidad_enemigos, nivel):
        return cantidad_enemigos < self.maximo_enemigos(nivel)

    def debe_generar_elite(self, tiempo_supervivencia, enemigos, nivel):
        if tiempo_supervivencia < self.proximo_elite:
            return False

        if any(enemigo.es_elite for enemigo in enemigos):
            return False

        # Las élites aparecen con menos espera conforme avanza la partida,
        # pero nunca más rápido que una por 45 segundos.
        self.proximo_elite = tiempo_supervivencia + max(45.0, 80.0 - nivel * 2.0)
        return True
