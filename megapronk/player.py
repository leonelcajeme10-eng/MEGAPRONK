import pygame
import math
from prong import Especial, Principal
from camara import Camara

class Player:
    def __init__(self):
        self.x = 700
        self.y = 700
        self.vida = 100
        self.mana = 100
        self.dx = 0
        self.dy = 0
        self.tamano_x = 50
        self.tamano_y = 50
        self.speed = 16
        self.dt = 1
        self.boton_x =False
        self.boton_y = False
        self.esp = Especial()
        self.principal = Principal()
    
    def input(self,camara):
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
            self.lanzarEspecial(camara)
        
        # Click izquierdo para ataque principal
        if botones[0]:
            self.ataquePrincipal()
        
    def lanzarEspecial(self,camara):
        mouse = pygame.mouse.get_pos()
        mouse_mundo = [mouse[0] + camara.x, mouse[1] + camara.y]
        centro = [self.x + self.tamano_x / 2, self.y + self.tamano_y / 2]
        dir = math.atan2(mouse_mundo[1] - centro[1], mouse_mundo[0] - centro[0])
        self.esp.nuevoProyectil(dir, [centro[0] + math.cos(dir) * 40, centro[1] + math.sin(dir) * 40 ])

    def ataquePrincipal(self):
        # usar la posición central del jugador para crear la hitbox
        center = [self.x + 25, self.y + 25]
        self.principal.atacar(center)

    def movimiento(self,mapa_rect):
        if self.dy != 0 and self.dx != 0:
            self.dx *= 0.7071
            self.dy *= 0.7071

        if self.dx != 0:
            self.x += self.dx
            self.boton_x = True
            self.colisiones(mapa_rect)

        if self.dy != 0:
            self.y += self.dy
            self.boton_y = True
            self.colisiones(mapa_rect)


    def colisiones(self,mapa_rect):

        jugador_rect = pygame.Rect(self.x,self.y,self.tamano_x,self.tamano_y)


        if self.boton_x == True:
            self.boton_x = False
            for pared in mapa_rect:
                if jugador_rect.colliderect(pared):
                    if self.dx > 0:
                        self.x = pared.left - self.tamano_x
                    elif self.dx < 0:
                        self.x = pared.right 
        

        if self.boton_y == True:
            self.boton_y = False  
            for pared in mapa_rect:
                if jugador_rect.colliderect(pared):
                    if self.dy > 0:
                        self.y = pared.top - self.tamano_y
                    elif self.dy < 0:
                        self.y = pared.bottom

    def seguimiento_camara(self):
        pass


        
    def update(self, dt,mapa,camara):
        self.input(camara)
        self.movimiento(mapa.paredes)
        self.esp.update(dt)
        self.principal.update(dt, [self.dx, self.dy])
    
    def dibujar(self,pantalla,camara):
        pygame.draw.rect(pantalla,"red",(self.x - camara.x,self.y - camara.y,self.tamano_x,self.tamano_y))
        for x in self.esp.proyectiles:
            pygame.draw.rect(pantalla,"blue",(x.posicion[0] - x.dimension[0] /2 - camara.x, x.posicion[1] - x.dimension[1] /2 - camara.y, x.dimension[0], x.dimension[1]))
        
        for x in self.principal.hitbox:
            pygame.draw.rect(pantalla,"blue",(x.posicion[0] - x.dimension[0] /2 - camara.x, x.posicion[1] - x.dimension[1] /2 - camara.y, x.dimension[0], x.dimension[1]))
