import pygame
import math
from prong import Especial

class Player:
    def __init__(self):
        self.x =  100
        self.y = 100
        self.vida = 100
        self.mana = 100
        self.dx = 0
        self.dy = 0
        self.speed = 20
        self.dt = 1
        self.esp = Especial()
    
    def input(self):
        keys = pygame.key.get_pressed()

        self.dx = 0
        self.dy = 0

        if keys[pygame.K_a]:
            self.dx = -self.speed

        if keys[pygame.K_d]:
            self.dx = self.speed

        if keys[pygame.K_w]:
            self.dy = -self.speed

        if keys[pygame.K_s]:
            self.dy = self.speed
        
        botones = pygame.mouse.get_pressed()

        # Click derecho
        if botones[2]:
            self.lanzarEspecial()
        
    def lanzarEspecial(self):
        mouse = pygame.mouse.get_pos()
        dir = math.atan2(mouse[1] - self.y, mouse[0] - self.x)
        self.esp.nuevoProyectil(dir, [self.x + 25 + math.cos(dir) * 40, self.y + 25 + math.sin(dir) * 40 ])

    def movimiento(self):
        if self.dy != 0 and self.dx != 0:

            self.dx *= 0.7071
            self.dy *= 0.7071
            self.x += self.dx 
            self.y += self.dy 
        else:
            self.x += self.dx
            self.y += self.dy

    def update(self, dt):
        self.input()
        self.movimiento()
        self.esp.update(dt)
    
    def dibujar(self,pantalla):
        pygame.draw.rect(pantalla,"red",(self.x,self.y,50,50))
        for x in self.esp.proyectiles:
            pygame.draw.circle(pantalla, "blue", x.posicion, x.radio)



