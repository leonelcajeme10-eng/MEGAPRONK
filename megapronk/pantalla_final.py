import pygame
import os
from player import Player
import random
ruta_actual = os.path.dirname(__file__)

class PantallaFinal:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.font_titulo = pygame.font.SysFont("Georgia", 80)
        self.font_texto = pygame.font.SysFont("Georgia", 42)
        self.font_chico = pygame.font.SysFont("Georgia", 32)
        self.rango_s = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "rango_s.png")).convert_alpha()
        self.rango_s = pygame.transform.smoothscale(self.rango_s, (250,250))
        self.rango_a = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "rango_a.png")).convert_alpha()
        self.rango_a = pygame.transform.smoothscale(self.rango_a, (250,250))
        self.rango_b = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "rango_b.png")).convert_alpha()
        self.rango_b = pygame.transform.smoothscale(self.rango_b, (250,250))
        self.rango_c = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "rango_c.png")).convert_alpha()
        self.rango_c = pygame.transform.smoothscale(self.rango_c, (250,250))
        self.marco = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "marco_final.png")).convert_alpha()
        self.marco = pygame.transform.smoothscale(self.marco, (700,850))
        self.boton_salir = pygame.Rect(self.ancho // 2 - 150, 940, 300, 75)
        self.particulas = []

        for i in range(80):
            self.particulas.append([
                random.randint(0, ancho),
                random.randint(0, alto),
                random.randint(2, 5),
                random.uniform(20, 70)
            ])
            
    def actualizar(self, dt):
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
            
    def manejar_evento(self, evento):
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()

            if self.boton_salir.collidepoint(mouse):
                return "salir"

        return None
            
    def calcular_rango(self, jugador, tiempo_total):
        puntos = 0
        puntos += jugador.kills * 2
        puntos += jugador.nivel * 10
        puntos += int(tiempo_total)

        if puntos >= 500:
            return "S"
        elif puntos >= 350:
            return "A"
        elif puntos >= 200:
            return "B"
        else:
            return "C"
        
    def dibujar(self, pantalla, jugador):
        self.dibujar_fondo_difuminado(pantalla)
        self.dibujar_particulas(pantalla)

        marco_rect = self.marco.get_rect(center=(self.ancho // 2, self.alto // 2))

        fondo_marco = pygame.Rect(marco_rect.x + 35, marco_rect.y + 55, marco_rect.width - 70, marco_rect.height - 125)

        pygame.draw.rect(pantalla, (12, 8, 14), fondo_marco, border_radius=25)
        pygame.draw.rect(pantalla, (70, 45, 25), fondo_marco, 3, border_radius=25)

        pantalla.blit(self.marco, marco_rect)

        titulo = self.font_titulo.render("RESULTADOS", True, (230, 200, 120))
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 80)))

        minutos = int(jugador.tiempo // 60)
        segundos = int(jugador.tiempo % 60)

        textos = [
            f"Tiempo total: {minutos:02d}:{segundos:02d}",
            f"Nivel total: {jugador.nivel}",
            f"Kills: {jugador.kills}"
        ]

        y = 280

        for texto in textos:
            render = self.font_texto.render(texto, True, (255, 240, 180))
            pantalla.blit(render, render.get_rect(center=(self.ancho // 2, y)))
            y += 60

        texto_prongs = self.font_texto.render("Pronks", True, (230, 200, 120))
        pantalla.blit(texto_prongs, texto_prongs.get_rect(center=(self.ancho // 2, y + 20)))

        y += 80

        for especial in jugador.prong.prongs:
            if "BolaFuego" == especial.Prong.__class__.__name__:
                nombre = "Bola de Fuego"
            elif "Prong" == especial.Prong.__class__.__name__:
                nombre = "Flecha"
            elif "ProngBomba" == especial.Prong.__class__.__name__:
                nombre = "Explosion"
                
            nivel = especial.nivel

            texto = self.font_chico.render(f"{nombre}: Nivel {nivel}", True, (255, 255, 255))
            pantalla.blit(texto, texto.get_rect(center=(self.ancho // 2, y)))

            y += 45

        rango = self.calcular_rango(jugador, jugador.tiempo)

        if rango == "S":
            imagen_rango = self.rango_s
        elif rango == "A":
            imagen_rango = self.rango_a
        elif rango == "B":
            imagen_rango = self.rango_b
        else:
            imagen_rango = self.rango_c

        pantalla.blit(imagen_rango, imagen_rango.get_rect(center=(self.ancho // 2, 720)))

        mouse = pygame.mouse.get_pos()
        hover = self.boton_salir.collidepoint(mouse)

        if hover:
            color_fondo = (75, 35, 35)
            color_borde = (255, 225, 140)
            color_texto = (255, 255, 210)
        else:
            color_fondo = (40, 20, 20)
            color_borde = (230, 200, 120)
            color_texto = (255, 240, 180)

        pygame.draw.rect(pantalla, color_fondo, self.boton_salir, border_radius=18)
        pygame.draw.rect(pantalla, color_borde, self.boton_salir, 4, border_radius=18)

        texto_salir = self.font_texto.render("SALIR", True, color_texto)
        pantalla.blit(texto_salir, texto_salir.get_rect(center=self.boton_salir.center))