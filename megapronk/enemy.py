import pygame
from player import Player
import math


class Enemy:
        def __init__(self):
            self.x = 50
            self.y = 50
            self.dx = 0
            self.dy = 0
            self.boton_x = False
            self.boton_y = False
            self.tamano_x = 50
            self.tamano_y = 50
            
            self.speed = 75


        def movimiento(self,jugador,dt,mapa_rect):
            self.dx = 0
            self.dy = 0
            self.dx = jugador.x - self.x
            self.dy = jugador.y - self.y

            distancia = (self.dx**2 + self.dy**2) ** 0.5

            if distancia != 0:
                self.dx /= distancia
                self.dy /= distancia

            mov_x = self.dx * self.speed * dt
            mov_y = self.dy * self.speed * dt    
            
            self.y += mov_y
            

            if mov_x != 0:
                self.x += mov_x
                self.boton_x = True
                self.colisiones(mapa_rect)

            if mov_y != 0:
                self.x += mov_x
                self.boton_y = True
                self.colisiones(mapa_rect)
            

        
        def colisiones(self,mapa_rect):

            enemigo_rect = pygame.Rect(self.x,self.y,self.tamano_x,self.tamano_y)

            if self.boton_x == True:
                self.boton_x = False
                for pared in mapa_rect:
                    if enemigo_rect.colliderect(pared):
                        if self.dx > 0:
                            self.x = pared.left - self.tamano_x
                        elif self.dx < 0:
                            self.x = pared.right 
            

            if self.boton_y == True:
                self.boton_y = False  
                for pared in mapa_rect:
                        if enemigo_rect.colliderect(pared):
                            if self.dy > 0:
                                self.y = pared.top - self.tamano_y
                            elif self.dy < 0:
                                self.y = pared.bottom

        
    
            

        
        def update(self,jugador,dt,mapa):
            self.movimiento(jugador,dt,mapa.paredes)


        
        def dibujar(self,pantalla,camara):
            pygame.draw.rect(pantalla,"red",(self.x - camara.x,self.y - camara.y,self.tamano_x,self.tamano_y))



            


            
        

