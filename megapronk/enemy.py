import pygame
from player import Player
import math
import random
from camara import Camara


class Enemy:
        def __init__(self,camara):
            self.x = 50
            self.y = 50
            self.dx = 0
            self.dy = 0
            self.boton_x = False
            self.boton_y = False
            self.tamano_x = 50
            self.tamano_y = 50
            self.vida = 100
            self.inmunidad = 60
            
            self.aparicion_enemigos(camara)
            
            self.speed = 120


        def aparicion_enemigos(self,camara):

            borde_izq = camara.x 
            borde_derecha = camara.x + camara.ancho
            borde_arriba = camara.y 
            borde_abajo = camara.y + camara.alto

            lado = random.choice(["izq","dere","arriba","abajo"])

            if lado == "izq":
                self.x = borde_izq - 100
                self.y = random.randint(int(borde_arriba), int(borde_abajo))
            if lado == "dere":
                self.x = borde_derecha + 100
                self.y = random.randint(int(borde_arriba), int(borde_abajo))
            if lado == "arriba":
                self.y = borde_arriba - 100
                self.x = random.randint(int(borde_izq), int(borde_derecha))
            if lado == "abajo":
                self.y = borde_abajo + 100
                self.x = random.randint(int(borde_izq), int(borde_derecha))



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
            
            if mov_x != 0:
                self.x += mov_x
                self.boton_x = True
                self.colisiones(mapa_rect)

            if mov_y != 0:
                self.y += mov_y
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

            

        def cooldown_golpe(self,jugador):
            enemigo_rect = pygame.Rect(self.x,self.y,self.tamano_x,self.tamano_y)
            jugador_rect = pygame.Rect(jugador.x,jugador.y,jugador.tamano_x,jugador.tamano_y)

            if self.inmunidad > 0:
                self.inmunidad -= 1

            if jugador_rect.colliderect(enemigo_rect) and self.inmunidad <= 0:
                self.inmunidad = 60
                jugador.vida -= 10
                



            

    
            
        def update(self,jugador,dt,mapa,camara):
            
            self.movimiento(jugador,dt,mapa.paredes)
            self.cooldown_golpe(jugador)
            


        
        def dibujar(self,pantalla,camara):
            pygame.draw.rect(pantalla,"red",(self.x - camara.x,self.y - camara.y,self.tamano_x,self.tamano_y))



            


            
        

