import pygame
from player import Player
from enemy import Enemy
from mapa import Mapa

pygame.init()


pantalla = pygame.display.set_mode((1920,1080))

clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

jugador = Player()
enemigo = Enemy()
mapa = Mapa()

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        print(evento)
        if evento.type == pygame.QUIT:
            ejecutando = False
        

    dt = clock.tick(60) / 1000.0

    pantalla.fill((30, 30, 30))

    
    
    mapa.update(pantalla,jugador)
    jugador.update(dt,mapa)
    enemigo.update(jugador,dt)
    jugador.dibujar(pantalla)
    enemigo.dibujar(pantalla)
    pygame.display.flip()

    

pygame.quit()


