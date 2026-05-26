import pygame
from player import Player
from enemy import Enemy
from mapa import Mapa
from camara import Camara
from prong import Proyectil, ProyectilOscilante
from ui import UI

pygame.init()

pantalla = pygame.display.set_mode((1920,1080))

clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

jugador = Player()
enemigo = Enemy()
mapa = Mapa()
camara = Camara()
ui = UI()

jugador.agregarProng(pygame.K_1, Proyectil)
jugador.agregarProng(pygame.K_2, ProyectilOscilante)

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


