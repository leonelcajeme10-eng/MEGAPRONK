import pygame
import os
from prong import Prong, BolaFuego, ProngBomba
import math

ruta_actual = os.path.dirname(__file__)


class UI:
    BASE_ANCHO = 1920
    BASE_ALTO = 1080

    def __init__(self):
        self.ruta_fuente = os.path.join(
            ruta_actual,
            "assets",
            "fonts",
            "Cinzel-VariableFont_wght.ttf"
        )

        # Imágenes originales
        self.marco_hp_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "vida_ui.png")
        ).convert_alpha()

        self.marco_exp_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "exp_ui.png")
        ).convert_alpha()

        self.marco_lvl_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "lvl_ui.png")
        ).convert_alpha()

        self.marco_kills_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "kills_ui.png")
        ).convert_alpha()

        self.logo_kills_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "logo_kills.png")
        ).convert_alpha()

        self.pronks_ui_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "pronks_ui.png")
        ).convert_alpha()

        self.disparo_pronk_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "disparo_pronk.png")
        ).convert_alpha()

        self.bolafuego_pronk_original = pygame.image.load(
            os.path.join(ruta_actual, "assets", "ui", "bolafuego_pronk.png")
        ).convert_alpha()
        
        self.megapronk = pygame.image.load(os.path.join(ruta_actual, "assets", "ui", "megapronk.png")).convert_alpha()

        self.escala_actual = None
        self.preparar_escala(1)

    def calcular_escala(self, pantalla):
        escala_x = pantalla.get_width() / self.BASE_ANCHO
        escala_y = pantalla.get_height() / self.BASE_ALTO

        return min(escala_x, escala_y)

    def s(self, valor):
        return int(valor * self.escala_actual)

    def escalar_imagen(self, imagen, ancho, alto):
        return pygame.transform.smoothscale(
            imagen,
            (self.s(ancho), self.s(alto))
        )

    def preparar_escala(self, escala):
        self.escala_actual = escala

        self.font = pygame.font.Font(
            self.ruta_fuente,
            max(1, self.s(40))
        )

        self.font2 = pygame.font.Font(
            self.ruta_fuente,
            max(1, self.s(45))
        )

        self.marco_hp = self.escalar_imagen(
            self.marco_hp_original,
            520,
            270
        )

        self.marco_exp = self.escalar_imagen(
            self.marco_exp_original,
            1000,
            115
        )

        self.marco_lvl = self.escalar_imagen(
            self.marco_lvl_original,
            130,
            130
        )

        self.marco_kills = self.escalar_imagen(
            self.marco_kills_original,
            235,
            135
        )

        self.logo_kills = self.escalar_imagen(
            self.logo_kills_original,
            82,
            82
        )

        self.pronks_ui = self.escalar_imagen(
            self.pronks_ui_original,
            500,
            265
        )

        self.disparo_pronk = self.escalar_imagen(
            self.disparo_pronk_original,
            80,
            80
        )

        self.bolafuego_pronk = self.escalar_imagen(
            self.bolafuego_pronk_original,
            80,
            80
        )
        
        self.megapronk = self.escalar_imagen(
            self.megapronk,
            230,
            230
        )

    def actualizar_escala_si_cambio(self, pantalla):
        nueva_escala = self.calcular_escala(pantalla)

        if self.escala_actual is None:
            self.preparar_escala(nueva_escala)
            return

        if abs(nueva_escala - self.escala_actual) > 0.01:
            self.preparar_escala(nueva_escala)

    def dibujar_hud(self, pantalla, jugador):
        self.actualizar_escala_si_cambio(pantalla)

        self.dibujar_barra_vida(pantalla, jugador)
        self.dibujar_barra_exp(pantalla, jugador)
        self.dibujar_lvl(pantalla, jugador)
        self.dibujar_kills(pantalla, jugador)
        self.dibujar_tiempo(pantalla, jugador)
        self.dibujar_pronks(pantalla, jugador)

    def dibujar_barra_vida(self, pantalla, jugador):
        x = self.s(60)
        y = self.s(35)

        barra_x = x + self.s(126)
        barra_y = y + self.s(107)
        barra_ancho = self.s(375)
        barra_alto = self.s(36)

        porcentaje_vida = jugador.vida / jugador.vida_max
        porcentaje_vida = max(0, min(1, porcentaje_vida))

        ancho_actual = int(barra_ancho * porcentaje_vida)

        pygame.draw.rect(
            pantalla,
            (45, 20, 25),
            (barra_x, barra_y, barra_ancho, barra_alto)
        )

        pygame.draw.rect(
            pantalla,
            (190, 25, 40),
            (barra_x, barra_y, ancho_actual, barra_alto)
        )

        if ancho_actual > self.s(6):
            pygame.draw.rect(
                pantalla,
                (255, 120, 120),
                (
                    barra_x + self.s(3),
                    barra_y + self.s(3),
                    ancho_actual - self.s(6),
                    self.s(6)
                )
            )

        pantalla.blit(self.marco_hp, (x, y))

    def dibujar_barra_exp(self, pantalla, jugador):
        x = pantalla.get_width() // 2 - self.marco_exp.get_width() // 2
        y = self.s(18)

        barra_x = x + self.s(95)
        barra_y = y + self.s(35)
        barra_ancho = self.s(780)
        barra_alto = self.s(34)

        porcentaje_exp = jugador.exp / jugador.exp_max
        porcentaje_exp = max(0, min(1, porcentaje_exp))

        ancho_actual = int(barra_ancho * porcentaje_exp)

        pygame.draw.rect(
            pantalla,
            (45, 20, 25),
            (barra_x, barra_y, barra_ancho, barra_alto)
        )

        pygame.draw.rect(
            pantalla,
            (70, 120, 255),
            (barra_x, barra_y, ancho_actual, barra_alto)
        )

        if ancho_actual > self.s(4):
            pygame.draw.rect(
                pantalla,
                (150, 220, 255),
                (
                    barra_x + self.s(2),
                    barra_y + self.s(2),
                    ancho_actual - self.s(4),
                    self.s(5)
                )
            )

        pantalla.blit(self.marco_exp, (x, y))

    def dibujar_lvl(self, pantalla, jugador):
        x = pantalla.get_width() - self.s(490)
        y = self.s(110)

        nivel = self.font.render(
            f"LV {jugador.nivel}",
            True,
            (255, 255, 255)
        )

        pantalla.blit(self.marco_lvl, (x, y))

        nivel_rect = nivel.get_rect(
            center=(
                x + self.marco_lvl.get_width() // 2,
                y + self.marco_lvl.get_height() // 2
            )
        )

        pantalla.blit(nivel, nivel_rect)

    def dibujar_kills(self, pantalla, jugador):
        x = pantalla.get_width() - self.s(300)
        y = self.s(108)

        kills = self.font.render(
            f"{jugador.kills}",
            True,
            (255, 255, 255)
        )

        pantalla.blit(self.marco_kills, (x, y))
        pantalla.blit(self.logo_kills, (x + self.s(112), y + self.s(25)))
        pantalla.blit(kills, (x + self.s(42), y + self.s(40)))

    def dibujar_tiempo(self, pantalla, jugador):
        y = self.s(130)

        tiempo = self.font2.render(
            f"{jugador.obtener_tiempo()}",
            True,
            (255, 255, 255)
        )

        tiempo_rect = tiempo.get_rect(
            center=(pantalla.get_width() // 2, y + tiempo.get_height() // 2)
        )

        pantalla.blit(tiempo, tiempo_rect)

    def dibujar_pronks(self, pantalla, jugador):
        x = self.s(220)
        y = pantalla.get_height() - self.s(310)

        pantalla.blit(self.pronks_ui, (x, y))
        pantalla.blit(jugador.icono, (x-185, y+30))

        texto_jugador = self.font.render(f"LV {jugador.nivel_ataque}",True,(255, 240, 180))

        if jugador.kills >= 50:
            jugador.megapronk = 1

        if(jugador.megapronk):
            pantalla.blit(self.megapronk, (x+1450, y+30))
        else:
            porcentaje_megapronk = max(0, 1 - (jugador.kills / 50))

            pantalla.blit(self.megapronk, (x + 400, y + 30))

            pygame.draw.circle(
                pantalla,
                (0, 0, 0),
                (x + 1565, y + 145),
                128,
                18
            )

            pygame.draw.arc(
                pantalla,
                (120, 40, 180),
                (x + 1437, y + 17, 256, 256),
                -math.pi / 2,
                -math.pi / 2 + porcentaje_megapronk * 2 * math.pi,
                18
            )

            pygame.draw.arc(
                pantalla,
                (220, 120, 255),
                (x + 1437, y + 17, 256, 256),
                -math.pi / 2,
                -math.pi / 2 + porcentaje_megapronk * 2 * math.pi,
                5
            )

            pygame.draw.circle(
                pantalla,
                (255, 180, 255),
                (x + 1565, y + 17),
                6
            )
            
            
        pantalla.blit(texto_jugador, (x - 130, y + 210))

        for i, prong in enumerate(jugador.prong.prongs):
            slot_x = x + self.s(33) + i * self.s(165)
            slot_y = y + self.s(75)

            slot_ancho = self.s(100)
            slot_alto = self.s(100)

            icono = prong.Prong.icono

            icono = pygame.transform.smoothscale(
                icono,
                (
                    max(1, int(icono.get_width() * self.escala_actual)),
                    max(1, int(icono.get_height() * self.escala_actual))
                )
            )

            offset_x = 0
            offset_y = 0

            if isinstance(prong.Prong, BolaFuego) and (i == 0 or i == 1):
                offset_x = self.s(6)
                offset_y = self.s(2)

            icono_rect = icono.get_rect(
                center=(
                    slot_x + slot_ancho // 2 + offset_x,
                    slot_y + slot_alto // 2 + offset_y
                )
            )

            pantalla.blit(icono, icono_rect)
            
            texto_lvl = self.font.render(f"LV {prong.nivel}", True, (255, 240, 180))
            texto_rect = texto_lvl.get_rect(center=(slot_x + slot_ancho // 2 + 10, slot_y + slot_alto + self.s(35) +25))
            pantalla.blit(texto_lvl, texto_rect)

            if prong.cooldown > 0:
                porcentaje_cooldown = prong.cooldown / prong.cooldown_time
                porcentaje_cooldown = max(0, min(1, porcentaje_cooldown))

                alto_cd = int(slot_alto * porcentaje_cooldown)

                if alto_cd > 0:
                    overlay = pygame.Surface((slot_ancho, alto_cd),pygame.SRCALPHA)

                    overlay.fill((0, 0, 0, 150))

                    if i == 0:
                        pantalla.blit(overlay,(slot_x + self.s(9),slot_y + slot_alto - alto_cd))
                    else:
                        pantalla.blit(overlay,(slot_x,slot_y + slot_alto - alto_cd))