import pygame
import os 
ruta_actual = os.path.dirname(__file__)

class UI:
    def __init__(self):
        self.font = pygame.font.Font(
        os.path.join(ruta_actual, "assets", "fonts", "PRISTINA.ttf"), 30)
        self.marco_hp = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "vida_ui.png")
        ).convert_alpha()
        self.marco_hp = pygame.transform.scale(
        self.marco_hp,
        (400, 200))  
        self.marco_exp = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "exp_ui.png")
        ).convert_alpha()
        self.marco_exp = pygame.transform.scale(
        self.marco_exp,
        (700, 80)
        )
        self.marco_lvl = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "lvl_ui.png")
        ).convert_alpha()
        self.marco_lvl = pygame.transform.scale(
        self.marco_lvl,
        (100, 100)
        )
    
    def dibujar_hud(self, pantalla, jugador):
        self.dibujar_barra_vida(pantalla, jugador)
        self.dibujar_barra_exp(pantalla, jugador)
        self.dibujar_lvl(pantalla, jugador)
        
    def dibujar_barra_vida(self, pantalla, jugador):
        x = 250
        y = 200

        barra_x = x + 71
        barra_y = y + 21
        barra_ancho = 285
        barra_alto = 24

        porcentaje_vida = jugador.vida / jugador.vida_max
        porcentaje_vida = max(0, min(1, porcentaje_vida))

        ancho_actual = barra_ancho * porcentaje_vida

        pygame.draw.rect(pantalla, (45, 20, 25), (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(pantalla, (255, 0, 0), (barra_x, barra_y, ancho_actual, barra_alto))

        pantalla.blit(self.marco_hp, (x-19, y-62))

    def dibujar_barra_exp(self, pantalla, jugador):
        
        x = 600
        y = 100

        barra_x = x + 75
        barra_y = y + 25
        barra_ancho = 560
        barra_alto = 24

        porcentaje_exp = jugador.exp / jugador.exp_max
        porcentaje_exp = max(0, min(1, porcentaje_exp))

        ancho_actual = barra_ancho * porcentaje_exp
        
        pygame.draw.rect(
            pantalla,
            (45, 20, 25),
            (barra_x, barra_y, barra_ancho, barra_alto)
        )

         # exp actual
        pygame.draw.rect(
            pantalla,
            (56, 122, 255),
            (barra_x, barra_y, ancho_actual, barra_alto)
        )

        pantalla.blit(self.marco_exp, (x, y))
    
    def dibujar_lvl(self, pantalla, jugador):
        x = 470
        y = 110
        
        nivel = self.font.render(
        f"LV {jugador.nivel}",
        True,
        (255,255,255))
        
        pantalla.blit(self.marco_lvl, (x,y))
        pantalla.blit(nivel, (x+25, y+32))
        
        
        
        