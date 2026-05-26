import pygame
import math
from prong import Prongs, Principal
from camara import Camara

class Player:
    def __init__(self, mapa):
        self.x = 700
        self.y = 700
        self.vida = 80
        self.vida_max = 100
        self.mana = 100
        self.exp = 20
        self.exp_max = 100
        self.nivel = 0
        self.kills = 0
        self.tiempo = 0
        self.dx = 0
        self.dy = 0
        self.tamano_x = 50
        self.tamano_y = 50
        self.speed = 16
        self.dt = 1
        self.boton_x = False
        self.boton_y = False
        self.prong = Prongs(mapa)
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

        for prong in self.prong.prongs:
            if keys[prong.tecla]:
                self.lanzarEspecial(camara, prong)

        botones = pygame.mouse.get_pressed()

        if botones[0]:
            self.ataquePrincipal(camara)

    def agregarProng(self, tecla, especial):
        self.prong.asignarProng(tecla, especial)

    def lanzarEspecial(self, camara, especial):
        mouse = pygame.mouse.get_pos()
        mouse_mundo = [mouse[0] + camara.x, mouse[1] + camara.y]
        centro = [self.x + self.tamano_x / 2, self.y + self.tamano_y / 2]
        dir = math.atan2(mouse_mundo[1] - centro[1], mouse_mundo[0] - centro[0])
        especial.nuevoProyectil(dir, [centro[0] + math.cos(dir) * 40, centro[1] + math.sin(dir) * 40 ])

    def ataquePrincipal(self, camara):
        mouse = pygame.mouse.get_pos()
        mouse_mundo = [mouse[0] + camara.x, mouse[1] + camara.y]
        centro = [self.x + self.tamano_x / 2, self.y + self.tamano_y / 2]
        dir = math.atan2(mouse_mundo[1] - centro[1], mouse_mundo[0] - centro[0])
        grado = math.degrees(dir)
        grado = grado % 360

        if grado >= 45 and grado < 135:
            dir = math.pi / 2
        elif grado >= 135 and grado < 225:
            dir = math.pi
        elif grado >= 225 and grado < 315:
            dir = 3 * math.pi / 2
        else:
            dir = 0

        center = [self.x + 25, self.y + 25]
        self.principal.atacar(center, dir, [self.tamano_x, self.tamano_y])

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
        self.tiempo += dt
        self.input(camara)
        self.movimiento(mapa.paredes)
        for prongs in self.prong.prongs:
            prongs.update(dt)
        center = [self.x + self.tamano_x / 2, self.y + self.tamano_y / 2]
        self.principal.update(dt, center)
    
    def dibujar(self,pantalla,camara):
        pygame.draw.rect(pantalla,"red",(self.x - camara.x,self.y - camara.y,self.tamano_x,self.tamano_y))
        for prong in self.prong.prongs:
            for x in prong.proyectiles:
                pygame.draw.rect(pantalla,"blue",camara.aplicar_rect(x.rectangulo))

        for x in self.principal.hitbox:
            pygame.draw.rect(pantalla,"blue",camara.aplicar_rect(x.rectangulo))
            
    def obtener_tiempo(self):
        minutos = int(self.tiempo) // 60
        segundos = int(self.tiempo) % 60
        
        return f"{minutos:02}:{segundos:02}"
                        