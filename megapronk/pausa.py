import pygame
import random
import os
ruta_actual = os.path.dirname(__file__)

class PauseMenu:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.pausado = False
        self.font_titulo = pygame.font.SysFont("Georgia", 90)
        self.font_boton = pygame.font.SysFont("Georgia", 45)
        self.botones = {
            "continuar": pygame.Rect(ancho//2 - 250, alto//2 - 30, 500, 80),
            "salir": pygame.Rect(ancho//2 - 250, alto//2 + 90, 500, 80)
        }
        self.borde_menu = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "borde_pausa.png"))
        self.borde_menu = pygame.transform.smoothscale(self.borde_menu, (925,575))
        self.particulas = []

        for i in range(80):
            self.particulas.append([
                random.randint(0, ancho),
                random.randint(0, alto),
                random.randint(2, 5),
                random.uniform(20, 70)
            ])

    def manejar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado

        if self.pausado and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if self.botones["continuar"].collidepoint(mouse):
                self.pausado = False

            if self.botones["salir"].collidepoint(mouse):
                return "salir"

        return None

    def actualizar(self, dt):
        if not self.pausado:
            return

        for p in self.particulas:
            p[1] -= p[3] * dt

            if p[1] < -10:
                p[0] = random.randint(0, self.ancho)
                p[1] = self.alto + 10

    def dibujar_fondo_difuminado(self, pantalla):
        copia = pantalla.copy()

        pequeño = pygame.transform.smoothscale(copia, (self.ancho // 12, self.alto // 12))
        blur = pygame.transform.smoothscale(pequeño, (self.ancho, self.alto))

        pantalla.blit(blur, (0, 0))

        oscuro = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        oscuro.fill((0, 0, 0, 120))
        pantalla.blit(oscuro, (0, 0))

    def dibujar_particulas(self, pantalla):
        for x, y, radio, velocidad in self.particulas:
            pygame.draw.circle(pantalla,(212, 175, 55), (int(x), int(y)), radio)

    def dibujar_boton(self, pantalla, rect, texto):
        mouse = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse)

        color_fondo = (25, 20, 15)
        color_borde = (255, 210, 80) if hover else (160, 120, 40)

        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)
        pygame.draw.rect(pantalla, color_borde, rect, width=4, border_radius=12)

        render = self.font_boton.render(texto, True, (255, 240, 200))
        pantalla.blit(render, (rect.centerx - render.get_width() // 2, rect.centery - render.get_height() // 2))

    def dibujar(self, pantalla):
        if not self.pausado:
            return

        self.dibujar_fondo_difuminado(pantalla)
        self.dibujar_particulas(pantalla)

        # Marco grande
        borde_x = self.ancho // 2 - 452
        borde_y = self.alto // 2 - 300

        # Cuadro negro interno
        menu = pygame.Rect(
        self.ancho // 2 - 407,
        self.alto // 2 - 258,835, 491)

        pygame.draw.rect(pantalla, (10, 8, 8), menu, border_radius=18)

        pantalla.blit(self.borde_menu, (borde_x, borde_y))

        titulo = self.font_titulo.render("PAUSA", True, (212, 175, 55))
        pantalla.blit(titulo, (menu.centerx - titulo.get_width() // 2,menu.y + 45))

        self.dibujar_boton(pantalla, self.botones["continuar"], "CONTINUAR")
        self.dibujar_boton(pantalla, self.botones["salir"], "SALIR")