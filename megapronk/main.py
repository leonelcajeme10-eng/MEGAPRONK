import pygame
from player import Player
from enemy import Enemy
from mapa import Mapa
from camara import Camara
from prong import Prong, BolaFuego
from ui import UI
from pausa import PauseMenu

pygame.init()

pantalla = pygame.display.set_mode((1920,1080))

clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

mapa = Mapa()
jugador = Player(mapa)
enemigo = Enemy()
camara = Camara()
ui = UI()
pause = PauseMenu(1920, 1080)

jugador.agregarProng(pygame.K_1, BolaFuego)
jugador.agregarProng(pygame.K_2, Prong)
jugador.agregarProng(pygame.K_3, Prong)

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        print(evento)
        if evento.type == pygame.QUIT:
            ejecutando = False
        accion = pause.manejar_evento(evento)
        if accion == "salir":
            ejecutando = False

    dt = clock.tick(60) / 1000.0

    if not pause.pausado:
        jugador.update(dt, mapa, camara)
        enemigo.update(jugador, dt, mapa)
        camara.update(jugador, dt)
    else:
        pause.actualizar(dt)

    pantalla.fill((255, 255, 255))

    mapa.update(pantalla,camara)
    jugador.dibujar(pantalla,camara)
    enemigo.dibujar(pantalla,camara)
    ui.dibujar_hud(pantalla, jugador)
    pause.dibujar(pantalla)
    pygame.display.flip()

    

pygame.quit()


