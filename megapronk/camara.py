import pygame



class Camara:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.ancho = 1920
        self.alto = 1080
        self.suavizado = 8

    def update(self, jugador, dt):

        objetivo_x = jugador.x + jugador.tamano_x / 2 - self.ancho / 2
        objetivo_y = jugador.y + jugador.tamano_y / 2 - self.alto / 2

        factor = min(1, self.suavizado * dt)
        self.x += (objetivo_x - self.x) * factor
        self.y += (objetivo_y - self.y) * factor

    def aplicar_rect(self, rect):
        return pygame.Rect(rect.x - self.x, rect.y - self.y, rect.width, rect.height)
    

    



