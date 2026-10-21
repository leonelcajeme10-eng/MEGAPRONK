import pygame


class TextoDanio:
    COLOR_CRITICO = (180, 0, 255)

    def __init__(self, posicion, danio, color=(255, 255, 255)):
        self.x, self.y = posicion
        self.tiempo_restante = 1.0

        tamano_fuente = 30 if color == self.COLOR_CRITICO else 24
        fuente = pygame.font.Font(None, tamano_fuente)
        texto = f"{danio:g}"
        self.sombra = fuente.render(texto, True, (30, 30, 30))
        self.imagen = fuente.render(texto, True, color)

    def actualizar(self, dt):
        self.tiempo_restante -= dt
        return self.tiempo_restante > 0

    def dibujar(self, pantalla, camara):
        x = int(self.x - camara.x - self.imagen.get_width() / 2)
        y = int(self.y - camara.y - self.imagen.get_height() / 2)
        pantalla.blit(self.sombra, (x + 1, y + 1))
        pantalla.blit(self.imagen, (x, y))
