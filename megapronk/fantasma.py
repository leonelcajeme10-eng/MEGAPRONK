import pygame
from enemy import Enemy

import math
class Fantasma(Enemy):
    COLOR = "white"
    SPEED = 100
    VIDA = 100
    DAMAGE = 10
    TAMANO_X = 50
    TAMANO_Y = 50
    EXP = 30
    ANIMACION_MOVIMIENTO = {
        "ruta": "assets/images/ghost_spritesheet.png",
        "columnas": 4,
        "filas": 4,
        "escala": 1,
        "velocidad": 0.12,
        "orden_filas": ["up", "down", "left", "right"]
    }

    def __init__(self, camara):
        super().__init__(camara)
        self.pararse = False
        
    def cooldown_golpe(self,jugador,proyectiles,mapa_rect):
        enemigo_rect = pygame.Rect(self.x,self.y,self.tamano_x,self.tamano_y)
        jugador_rect = pygame.Rect(jugador.x,jugador.y,jugador.tamano_x,jugador.tamano_y)

        if self.inmunidad > 0:
            self.inmunidad -= 1

        

        if self.distancia < 400:
            if self.inmunidad <= 0:
                self.inmunidad = 60
                self.ataque_enemigo(jugador,proyectiles,mapa_rect)
            


    def movimiento(self,jugador,dt,mapa_rect):

        
            self.dx = 0
            self.dy = 0

            self.dx = jugador.x - self.x
            self.dy = jugador.y - self.y

            self.distancia = (self.dx**2 + self.dy**2) ** 0.5

            
            

            if self.distancia != 0:
                self.dx /= self.distancia
                self.dy /= self.distancia
                self.actualizar_direccion_animacion()


            if self.distancia > 400:
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
        

    
    def ataque_enemigo(self,jugador,proyectiles,mapa_rect):
            enemigo_rect = pygame.Rect(self.x,self.y,self.tamano_x,self.tamano_y)
            jugador_rect = pygame.Rect(jugador.x,jugador.y,jugador.tamano_x,jugador.tamano_y)

            centro_x = self.x + self.tamano_x/2
            centro_y = self.y + self.tamano_y/2


            direccion = math.atan2(self.dy,self.dx)

            proyectil = Proyectil_enemigo(direccion,self.damage,10,12,centro_x,centro_y)
            proyectiles.append(proyectil)
        


    def update(self,jugador,dt,mapa,camara,enemigos,proyectiles):
            
        self.movimiento(jugador,dt,mapa.paredes)
        self.cooldown_golpe(jugador,proyectiles,mapa.paredes)
        self.separar_enemigos(enemigos)

        if self.animador is not None:
            self.animador.update(dt)

        if self.vida <= 0:
            jugador.exp += self.experiencia
            jugador.megapronk += 1
            enemigos.remove(self)
            jugador.kills += 1
            

class Proyectil_enemigo:
    def __init__(self,direccion,damage,velocidad,tamano,x,y):
        self.x = x
        self.y = y
        self.dir = direccion
        self.damage = damage
        self.velocidad = velocidad
        self.tamano = tamano
        self.tiempo_vida = 2.0
        

    def dibujar(self, pantalla, camara):
        proyectil_rect = pygame.Rect(self.x - camara.x,self.y - camara.y,self.tamano,self.tamano)
        pygame.draw.rect(pantalla,"yellow",proyectil_rect)

    
    def colisiones_pared(self,mapa_paredes,proyectiles,camara):
        proyectil_rect = pygame.Rect(self.x - camara.x,self.y - camara.y,self.tamano,self.tamano)

        for pared in mapa_paredes:
            if proyectil_rect.colliderect(pared):
                proyectiles.remove(self)
                break
    
    def colision_jugador(self,jugador,camara,proyectiles):
        proyectil_rect = pygame.Rect(self.x - camara.x,self.y - camara.y,self.tamano,self.tamano)
        jugador_rect = pygame.Rect(jugador.x - camara.x,jugador.y - camara.y,jugador.tamano_x,jugador.tamano_y)

        if proyectil_rect.colliderect(jugador_rect):
            jugador.vida -= self.damage
            proyectiles.remove(self)
            

    def desaparecer_bala(self,dt,proyectiles):

        self.tiempo_vida -= dt

        if self.tiempo_vida <= 0:
            proyectiles.remove(self)
            return True 

        return False


    def update(self,mapa,proyectiles,camara,dt,jugador):
        
        if self.desaparecer_bala(dt,proyectiles):
            return
        
        self.x += math.cos(self.dir) * self.velocidad
        self.y += math.sin(self.dir) * self.velocidad
        self.colision_jugador(jugador,camara,proyectiles)
        self.colisiones_pared(mapa.paredes,proyectiles,camara)
        
