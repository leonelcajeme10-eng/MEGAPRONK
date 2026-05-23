import pygame

class Player:
    def __init__(self):
        self.x =  100
        self.y = 100
        self.vida = 100
        self.mana = 100
        self.dx = 0
        self.dy = 0
        self.speed = 1.8
    
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
        
    
    def movimiento(self,dt):
        if self.dy != 0 and self.dx != 0:

            self.dx *= 0.7071
            self.dy *= 0.7071
            self.x += self.dx * dt
            self.y += self.dy * dt
        else:
            self.x += self.dx
            self.y += self.dy

    def update(self):
        self.input()
        self.movimiento()
    
    def dibujar(self,pantalla):
        pygame.draw.rect(pantalla,"red",(self.x,self.y,50,50))



