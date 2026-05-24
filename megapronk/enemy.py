import pygame
from player import Player
import math


class Enemy:
        def __init__(self):
            self.x = 50
            self.y = 50
            self.dx = 0
            self.dy = 0
            self.speed = 75
            self.leoneo = "pedofilo"
        def movimiento(self,jugador,dt):
            self.dx = jugador.x - self.x
            self.dy = jugador.y - self.y

            distancia = (self.dx**2 + self.dy**2) ** 0.5

            if distancia != 0:
                self.dx /= distancia
                self.dy /= distancia

            self.x += self.dx * self.speed * dt
            self.y += self.dy * self.speed * dt

        
        def update(self,jugador,dt):
            self.movimiento(jugador,dt)

        
        def dibujar(self,pantalla):
            pygame.draw.rect(pantalla,"red",(self.x,self.y,50,50))



            


            
        

