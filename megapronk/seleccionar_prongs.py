import pygame
import random
import os
import math
import player
ruta_actual = os.path.dirname(__file__)
from prong import Prong, BolaFuego, ProngBomba

class SeleccionarProngs:
    def __init__(self):
        self.opciones = []
        self.activo = False
        self.opciones = ["Bola de Fuego", "Disparo", "Explosion"]
        self.cartas = []
        self.font_titulo = pygame.font.SysFont("Georgia", 60)
        self.font_texto = pygame.font.SysFont("Georgia", 32)
        self.ancho = 1920
        self.alto = 1080
        self.cont = 0
        self.slot_actual = 0
        teclas = [pygame.K_1, pygame.K_2, pygame.K_3]
        
    def abrir(self):
        if self.cont < 3:
            self.activo = True

        
    def cerrar(self):
        self.activo = False
        
    def manejar_evento(self, evento, jugador):
        if not self.activo:
            return None
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            teclas = [pygame.K_1, pygame.K_2, pygame.K_3][self.slot_actual]
            for i, rect in enumerate(self.cartas):
                if rect.collidepoint(mouse):
                    if self.cont < 3:
                        if self.opciones[i] == "Bola de Fuego":
                            jugador.agregarProng(teclas, BolaFuego)
                        elif self.opciones[i] == "Disparo":
                            jugador.agregarProng(teclas, Prong)
                        elif self.opciones[i] == "Explosion":
                            jugador.agregarProng(teclas, ProngBomba)
                            
                        self.cont += 1
                        self.slot_actual += 1
                        self.cerrar()
                        return self.opciones[i]                     
        return None
                        
    def dibujar(self, pantalla):
        if not self.activo:
            return

        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0, 0))

        titulo = self.font_titulo.render("Elige un Prong", True, (230, 200, 120))
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 180)))

        self.cartas = []

        x_inicial = self.ancho // 2 - 480
        y = 320

        for i, nombre in enumerate(self.opciones):
            rect = pygame.Rect(x_inicial + i * 340, y, 280, 380)
            self.cartas.append(rect)

            pygame.draw.rect(pantalla, (20, 18, 30), rect, border_radius=25)
            pygame.draw.rect(pantalla, (210, 160, 60), rect, 4, border_radius=25)

            texto = self.font_texto.render(nombre, True, (255, 240, 180))
            pantalla.blit(texto, texto.get_rect(center=(rect.centerx, rect.centery)))