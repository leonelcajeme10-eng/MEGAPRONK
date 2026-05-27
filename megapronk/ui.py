import pygame
import os 
from prong import Prong, BolaFuego
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
        
        self.pronks_ui = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "pronks_ui.png"))
        self.pronks_ui = pygame.transform.smoothscale(self.pronks_ui, (370,185))
        
        self.disparo_pronk = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "disparo_pronk.png"))
        self.disparo_pronk = pygame.transform.smoothscale(self.disparo_pronk, (80,80))
        
        self.bolafuego_pronk = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "bolafuego_pronk.png"))
        self.bolafuego_pronk = pygame.transform.smoothscale(self.bolafuego_pronk, (80,80))
    
    def dibujar_hud(self, pantalla, jugador):
        self.dibujar_barra_vida(pantalla, jugador)
        self.dibujar_barra_exp(pantalla, jugador)
        self.dibujar_lvl(pantalla, jugador)
        self.dibujar_kills(pantalla, jugador)
        self.dibujar_tiempo(pantalla, jugador)
        self.dibujar_pronks(pantalla, jugador)
        
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
        
    def dibujar_pronks(self, pantalla, jugador):
        x = 300
        y = 750 
        
        
        pantalla.blit(self.pronks_ui, (x, y))
        
        for i, prong in enumerate(jugador.prong.prongs):
            slot_x = x + 8 + i * 125
            slot_y = y + 38

            slot_ancho = 100
            slot_alto = 100

            icono = prong.Prong.icono

            offset_x = 0
            offset_y = 0

            if isinstance(prong.Prong, BolaFuego) and (i == 0 or i == 1):
                offset_x = +6
                offset_y = 2    

            icono_rect = icono.get_rect(
            center=(slot_x + slot_ancho // 2 + offset_x,
            slot_y + slot_alto // 2 + offset_y)
            )

            pantalla.blit(icono, icono_rect)
            
            if prong.cooldown > 0:
                porcentaje_cooldown = prong.cooldown / prong.cooldown_time
                alto_cd = slot_alto * porcentaje_cooldown

                overlay = pygame.Surface((slot_ancho, alto_cd), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))

                if i == 0:
                    pantalla.blit(overlay, (slot_x+9, slot_y + slot_alto - alto_cd))
                else:
                    pantalla.blit(overlay, (slot_x, slot_y + slot_alto - alto_cd))

            
        