import pygame
from player import Player
from enemy import Enemy
from mapa import Mapa
from camara import Camara
from prong import Prong, BolaFuego
from ui import UI

pygame.init()

pantalla = pygame.display.set_mode((1920,1080))

clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

mapa = Mapa()
jugador = Player(mapa)
enemigo = Enemy()
camara = Camara()
ui = UI()

jugador.agregarProng(pygame.K_1, BolaFuego)
jugador.agregarProng(pygame.K_2, Prong)
jugador.agregarProng(pygame.K_3, Prong)

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        print(evento)
        if evento.type == pygame.QUIT:
            ejecutando = False

    dt = clock.tick(60) / 1000.0

    jugador.update(dt,mapa,camara)
    enemigo.update(jugador,dt,mapa)
    camara.update(jugador,dt)

    pantalla.fill((30, 30, 30))

    mapa.update(pantalla,camara)
    jugador.dibujar(pantalla,camara)
    enemigo.dibujar(pantalla,camara)
    ui.dibujar_hud(pantalla, jugador)
    pygame.display.flip()

    

pygame.quit()


