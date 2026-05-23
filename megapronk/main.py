import pygame
from player import Player


pygame.init()

pantalla = pygame.display.set_mode((1920,1080))

clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

jugador = Player()

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        print(evento)
        if evento.type == pygame.QUIT:
            ejecutando = False
        

    
    pantalla.fill((30, 30, 30))

    jugador.update()
    jugador.dibujar(pantalla)
    pygame.display.flip()

    

pygame.quit()


