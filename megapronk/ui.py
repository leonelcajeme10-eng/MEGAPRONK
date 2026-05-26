import pygame
import os 
ruta_actual = os.path.dirname(__file__)

class UI:
    def __init__(self):
        self.font = pygame.font.Font(
        os.path.join(ruta_actual, "assets", "fonts", "Cinzel-VariableFont_wght.ttf"), 30)
        self.font2 = pygame.font.Font(
        os.path.join(ruta_actual, "assets", "fonts", "Cinzel-VariableFont_wght.ttf"), 35)
        self.marco_hp = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "vida_ui.png")
        ).convert_alpha()
        self.marco_hp = pygame.transform.smoothscale(
        self.marco_hp,
        (400, 200))  
        self.marco_exp = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "exp_ui.png")
        ).convert_alpha()
        self.marco_exp = pygame.transform.smoothscale(
        self.marco_exp,
        (700, 80)
        )
        self.marco_lvl = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "lvl_ui.png")
        ).convert_alpha()
        self.marco_lvl = pygame.transform.smoothscale(
        self.marco_lvl,
        (100, 100)
        )
        self.marco_kills = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "kills_ui.png"))
        self.marco_kills = pygame.transform.smoothscale(self.marco_kills, (200, 100))
        
        self.logo_kills = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "logo_kills.png"))
        self.logo_kills = pygame.transform.smoothscale(self.logo_kills, (72, 72))
    
    def dibujar_hud(self, pantalla, jugador):
        self.dibujar_barra_vida(pantalla, jugador)
        self.dibujar_barra_exp(pantalla, jugador)
        self.dibujar_lvl(pantalla, jugador)
        self.dibujar_kills(pantalla, jugador)
        self.dibujar_tiempo(pantalla, jugador)
        
    def dibujar_barra_vida(self, pantalla, jugador):
        x = 220
        y = 140

        barra_x = x + 71
        barra_y = y + 21
        barra_ancho = 285
        barra_alto = 24

        porcentaje_vida = jugador.vida / jugador.vida_max
        porcentaje_vida = max(0, min(1, porcentaje_vida))

        ancho_actual = barra_ancho * porcentaje_vida

        pygame.draw.rect(pantalla, (45, 20, 25), (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(pantalla, (190, 25, 40), (barra_x, barra_y, ancho_actual, barra_alto))
        pygame.draw.rect(pantalla, (255, 120, 120), (barra_x + 3, barra_y + 3, ancho_actual - 6, 6))

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
        
        pygame.draw.rect(pantalla, (45, 20, 25), (barra_x, barra_y, barra_ancho, barra_alto))

         # exp actual
        pygame.draw.rect(pantalla, (70, 120, 255),(barra_x, barra_y, ancho_actual, barra_alto))
        pygame.draw.rect(pantalla, (150, 220, 255), (barra_x + 2, barra_y + 2, ancho_actual - 4, 5))   
        pantalla.blit(self.marco_exp, (x, y))
    
    def dibujar_lvl(self, pantalla, jugador):
        x = 1300
        y = 110
        
        nivel = self.font.render(
        f"LV {jugador.nivel}",
        True,
        (255,255,255))
        
        pantalla.blit(self.marco_lvl, (x,y))
        pantalla.blit(nivel, (x+19, y+30))
        
    def dibujar_kills(self, pantalla, jugador):
        x = 1450
        y = 110
        
        kills = self.font2.render(f"{jugador.kills}", True, (255,255,255))
        pantalla.blit(self.marco_kills, (x,y))
        pantalla.blit(self.logo_kills, (x+100, y+12))
        pantalla.blit(kills, (x+43, y+27))
        
    def dibujar_tiempo(self, pantalla, jugador):
        x = pantalla.get_width() / 2
        y = 170
        
        tiempo = self.font2.render(f"{jugador.obtener_tiempo()}", True, (255,255,255))
        pantalla.blit(tiempo, (x-50, y))
        
        
        