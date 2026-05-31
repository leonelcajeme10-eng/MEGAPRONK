import pygame
import os


SONIDOS = {}
ULTIMA_REPRODUCCION = {}


def cargar_sonidos(ruta_actual):
    rutas = {
        "prong_shoot": ("assets", "sounds", "disparo.ogg"),
        "fireball": ("assets", "sounds", "fireball.wav"),
        "bomb_shoot": ("assets", "sounds", "disparo.ogg"),
        "bomb_explosion": ("assets", "sounds", "bomb1.wav"),

        "enemy_hit": ("assets", "sounds", "hit.wav"),
        "slash": ("assets", "sounds", "slash.wav"),
        
        "level_up": ("assets", "sounds", "level_up.wav"),
    }

    for nombre, partes_ruta in rutas.items():
        ruta = os.path.join(ruta_actual, *partes_ruta)

        if os.path.exists(ruta):
            SONIDOS[nombre] = pygame.mixer.Sound(ruta)
        else:
            print("No se encontró el sonido:", ruta)


def play_sfx(nombre, volumen=1.0, cooldown_ms=0):
    if nombre not in SONIDOS:
        return

    tiempo_actual = pygame.time.get_ticks()

    if cooldown_ms > 0:
        ultimo = ULTIMA_REPRODUCCION.get(nombre, 0)

        if tiempo_actual - ultimo < cooldown_ms:
            return

        ULTIMA_REPRODUCCION[nombre] = tiempo_actual

    sonido = SONIDOS[nombre]
    sonido.set_volume(volumen)
    sonido.play()