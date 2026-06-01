import pygame
from player import Player
import math
import random
from camara import Camara
from anim import AnimadorMovimiento

class Enemy:
        COLOR = "red"
        SPEED = 120
        VIDA = 100
        DAMAGE = 10
        TAMANO_X = 50
        TAMANO_Y = 50
        EXP = 20 
        
        ANIMACION_MOVIMIENTO = None

        def __init__(self, camara):
            self.x = 50
            self.y = 50
            self.dx = 0
            self.dy = 0

            self.tamano_x = self.TAMANO_X
            self.tamano_y = self.TAMANO_Y

            self.vida = self.VIDA
            self.speed = self.SPEED
            self.damage = self.DAMAGE
            self.color = self.COLOR
            self.experiencia = self.EXP

            self.inmunidad = 60
            self.boton_x = False
            self.boton_y = False
            self.tiempo_golpe_visual = 0
            self.duracion_golpe_visual = 160
            self.ultima_vida = self.vida
            

            # Animación
            self.direccion = "down"
            self.animador = None

            if self.ANIMACION_MOVIMIENTO is not None:
                self.animador = AnimadorMovimiento(self.ANIMACION_MOVIMIENTO)

                imagen = self.animador.imagen_actual()
                self.tamano_x = imagen.get_width()
                self.tamano_y = imagen.get_height()
            
            self.aparicion_enemigos(camara)


        def aparicion_enemigos(self,camara):

            margen_spawn = 100
            borde_izq = camara.x 
            borde_derecha = camara.x + camara.ancho
            borde_arriba = camara.y 
            borde_abajo = camara.y + camara.alto

            lado = random.choice(["izq","dere","arriba","abajo"])

            if lado == "izq":
                self.x = borde_izq - self.tamano_x - margen_spawn
                self.y = random.randint(int(borde_arriba), int(borde_abajo))
            if lado == "dere":
                self.x = borde_derecha + margen_spawn
                self.y = random.randint(int(borde_arriba), int(borde_abajo))
            if lado == "arriba":
                self.y = borde_arriba - self.tamano_y - margen_spawn
                self.x = random.randint(int(borde_izq), int(borde_derecha))
            if lado == "abajo":
                self.y = borde_abajo + margen_spawn
                self.x = random.randint(int(borde_izq), int(borde_derecha))



        def movimiento(self,jugador,dt,mapa_rect):
            self.dx = 0
            self.dy = 0
            self.dx = jugador.x - self.x
            self.dy = jugador.y - self.y

            self.distancia = (self.dx**2 + self.dy**2) ** 0.5
            

            if self.distancia != 0:
                self.dx /= self.distancia
                self.dy /= self.distancia
                self.actualizar_direccion_animacion() ###
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

            self.enemigo_rect = pygame.Rect(self.x,self.y,self.tamano_x,self.tamano_y)

            if self.boton_x == True:
                self.boton_x = False
                for pared in mapa_rect:
                    if self.enemigo_rect.colliderect(pared):
                        if self.dx > 0:
                            self.x = pared.left - self.tamano_x
                        elif self.dx < 0:
                            self.x = pared.right 
            if self.boton_y == True:
                self.boton_y = False  
                for pared in mapa_rect:
                        if self.enemigo_rect.colliderect(pared):
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
                jugador.vida -= self.damage
    

        def separar_enemigos(self,enemigos):
            
            for otro_enemigo in enemigos:
                if otro_enemigo != self:
                    otro_enemigo.enemigo_rect = pygame.Rect(otro_enemigo.x,otro_enemigo.y,otro_enemigo.tamano_x,otro_enemigo.tamano_y)
                    
                    if otro_enemigo.enemigo_rect.colliderect(self.enemigo_rect):
                            distancia_x = otro_enemigo.x - self.x
                            distancia_y = otro_enemigo.y - self.y
                        
                            self.x -= distancia_x * 0.05

                            otro_enemigo.x += distancia_x * 0.05
                            self.y -= distancia_y * 0.05

                            otro_enemigo.x += distancia_y * 0.05


    
            
        def update(self,jugador,dt,mapa,camara,enemigos,proyectiles):
            
            self.movimiento(jugador,dt,mapa.paredes)
            self.cooldown_golpe(jugador)
            self.separar_enemigos(enemigos)

            if self.animador is not None:
                self.animador.update(dt)
        
            if self.vida < self.ultima_vida:
                self.tiempo_golpe_visual = pygame.time.get_ticks()
                self.ultima_vida = self.vida
            
            if self.vida <= 0:
                jugador.exp += self.experiencia
                jugador.megapronk += 1
                enemigos.remove(self)
                jugador.kills += 1
            
            

         
        
        def dibujar(self,pantalla,camara):
            draw_x = self.x - camara.x
            draw_y = self.y - camara.y

            golpeado = pygame.time.get_ticks() - self.tiempo_golpe_visual < self.duracion_golpe_visual

            if golpeado:
                draw_x += random.randint(-4, 4)
                draw_y += random.randint(-4, 4)

            if self.animador is not None:
                frame = self.animador.imagen_actual()
                if golpeado:
                    frame = frame.copy()
                    frame.fill((255, 80, 80, 0), special_flags=pygame.BLEND_RGBA_ADD)

                pantalla.blit(frame, (draw_x, draw_y))
                return

            color = self.color

            if golpeado:
                color = (255, 80, 80)

            pygame.draw.rect(
                pantalla,
                color,
                (
                    draw_x,
                    draw_y,
                    self.tamano_x,
                    self.tamano_y
                )
            )

        def actualizar_direccion_animacion(self):
            if abs(self.dx) > abs(self.dy):
                if self.dx > 0:
                    self.direccion = "right"
                else:
                    self.direccion = "left"
            else:
                if self.dy > 0:
                    self.direccion = "down"
                else:
                    self.direccion = "up"

            if self.animador is not None:
                self.animador.set_direccion(self.direccion)


        