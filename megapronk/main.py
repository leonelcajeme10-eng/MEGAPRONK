import pygame
from player import Player
from enemy import Enemy
from mapa import Mapa
from camara import Camara
from prong import Prong, BolaFuego
from ui import UI
from pausa import PauseMenu
from enemigo_mariposa import Mariposa
from fantasma import Fantasma

pygame.init()

pantalla = pygame.display.set_mode((1920,1080))

clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

mapa = Mapa()
jugador = Player(mapa)
camara = Camara()
ui = UI()

tiempo_spawn = 0
enemigos = []
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
    
    pause.actualizar(dt)

    if pause.pausado:
        pantalla.fill((255, 255, 255))
        mapa.update(pantalla, camara)
        jugador.dibujar(pantalla, camara)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla, camara)

        ui.dibujar_hud(pantalla, jugador)
        pause.dibujar(pantalla)

        pygame.display.flip()
        continue


    tiempo_spawn += dt
    if tiempo_spawn >= 1:
        enemigos.append(Fantasma(camara))
        enemigos.append(Mariposa(camara))
        tiempo_spawn = 0

    jugador.update(dt, mapa, camara)
    camara.update(jugador, dt, mapa)

    pantalla.fill((255, 255, 255))
    mapa.update(pantalla, camara)
    jugador.dibujar(pantalla, camara)

    for enemigo in enemigos:
        enemigo.update(jugador, dt, mapa, camara,enemigos)
        enemigo.dibujar(pantalla, camara)

    ui.dibujar_hud(pantalla, jugador)
    pause.dibujar(pantalla)

    pygame.display.flip()
    

pygame.quit()


