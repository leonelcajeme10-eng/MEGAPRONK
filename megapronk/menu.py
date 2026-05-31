import pygame
import random
import os
import math
ruta_actual = os.path.dirname(__file__)


class Menu:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.font_titulo = pygame.font.SysFont("Georgia", 90)
        self.font_boton = pygame.font.SysFont("Georgia", 45)
        self.fondo = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "fondo_menu.png")).convert()
        self.fondo = pygame.transform.smoothscale(self.fondo, (ancho, alto))
        self.logo = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "logo.png")).convert_alpha()
        self.logo = pygame.transform.smoothscale(self.logo, (625, 425))
        self.botones = {
            "jugar": pygame.Rect(ancho//2 - 250, alto//2 + 50, 500, 80),
            "salir": pygame.Rect(ancho//2 - 250, alto//2 + 220, 500, 80)
        }
        self.borde_menu = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "borde_pausa.png")
        ).convert_alpha()

        self.borde_menu = pygame.transform.smoothscale(
            self.borde_menu, (705, 450)
        )
        self.volumen = 0.8
        self.arrastrando_volumen = False
        self.barra_volumen = pygame.Rect(ancho - 260,alto - 60,200,10)

        self.particulas = []
        for i in range(80):
            self.particulas.append([
            random.randint(0, ancho),          # x
            random.randint(0, alto),           # y
            random.randint(2, 5),              # radio
            random.uniform(20, 70),            # velocidad_y
            random.uniform(-20, 20)            # velocidad_x
        ])

    def manejar_evento(self, evento):
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.botones["jugar"].collidepoint(evento.pos):
                return "jugar"

            if self.botones["salir"].collidepoint(evento.pos):
                return "salir"
            
        if evento.type == pygame.MOUSEBUTTONDOWN:        
            if self.barra_volumen.collidepoint(evento.pos):
                self.arrastrando_volumen = True

        if evento.type == pygame.MOUSEBUTTONUP:
            self.arrastrando_volumen = False

        if evento.type == pygame.MOUSEMOTION and self.arrastrando_volumen:
            mouse_x = evento.pos[0]
            self.volumen = (mouse_x - self.barra_volumen.x) / self.barra_volumen.width
            self.volumen = max(0, min(1, self.volumen))
        
        pygame.mixer.music.set_volume(self.volumen)

        return None

    def dibujar_particulas(self, pantalla):
        for x, y, radio, velocidad_y, velocidad_x in self.particulas:
            pygame.draw.circle(
                pantalla,
                (212, 175, 55),
                (int(x), int(y)),
                radio
            )
            
    def actualizar(self, dt):
         for particula in self.particulas:
            particula[0] += particula[4] * dt
            particula[1] += particula[3] * dt

            if particula[1] > self.alto:
                particula[0] = random.randint(0, self.ancho)
                particula[1] = -10
                particula[4] = random.uniform(-20, 20)

            if particula[0] < 0:
                particula[0] = self.ancho

            elif particula[0] > self.ancho:
                particula[0] = 0

    def dibujar_boton(self, pantalla, rect, texto):
        mouse = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse)

        color_fondo = (25, 20, 15)
        color_borde = (255, 210, 80) if hover else (160, 120, 40)

        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)
        pygame.draw.rect(pantalla, color_borde, rect, width=4, border_radius=12)

        render = self.font_boton.render(texto, True, (255, 240, 200))
        pantalla.blit(render,(rect.centerx - render.get_width() // 2, rect.centery - render.get_height() // 2))

    def dibujar(self, pantalla):
        pantalla.fill((5, 3, 8))
        pantalla.blit(self.fondo, (0, 0))
        self.dibujar_particulas(pantalla)

        borde_x = self.ancho // 2 - 350
        borde_y = self.alto // 2 - 60 
        
        logo_y_anim = math.sin(pygame.time.get_ticks() * 0.004) * 5
        menu = pygame.Rect(self.ancho // 2 - 320, self.alto // 2 - 30, 645, 390)
        pygame.draw.rect(pantalla, (10, 8, 8), menu, border_radius=18)
        pantalla.blit(self.borde_menu, (borde_x, borde_y))
        self.dibujar_boton(pantalla, self.botones["jugar"], "JUGAR")
        self.dibujar_boton(pantalla, self.botones["salir"], "SALIR")
        
        pantalla.blit(self.logo, (self.ancho // 2 - 310, self.alto//2 - 500 + logo_y_anim) )
        icono = self.font_boton.render("♪", True, (255, 210, 80))
        
        pantalla.blit(icono, (self.ancho - 180, self.alto - 115))
        texto_vol = self.font_boton.render(
            f"{int(self.volumen * 100)}%",
            True,
            (255, 240, 200)
        )

        pantalla.blit(
            texto_vol,
            (self.ancho - 360, self.alto - 85)
        )

        pygame.draw.rect(
            pantalla,
            (40, 30, 20),
            self.barra_volumen,
            border_radius=5
        )

        pygame.draw.rect(
            pantalla,
            (255, 210, 80),
            (
                self.barra_volumen.x,
                self.barra_volumen.y,
                int(self.barra_volumen.width * self.volumen),
                self.barra_volumen.height
            ),
            border_radius=5
        )

        pygame.draw.circle(
            pantalla,
            (255, 240, 200),
            (
                self.barra_volumen.x +
                int(self.barra_volumen.width * self.volumen),
                self.barra_volumen.centery
            ),
            10
        )
        
        