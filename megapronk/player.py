import pygame
import math
from prong import Prongs, Principal
from camara import Camara
import random
import os
ruta_actual = os.path.dirname(__file__)

class Player:
    def __init__(self, mapa):
        self.x = 700
        self.y = 700
        self.vida = 100
        self.vida_max = 100
        self.mana = 0
        self.exp = 99
        self.exp_max = 100
        self.nivel = 0
        self.kills = 0
        self.tiempo = 0
        self.dx = 0
        self.dy = 0
        self.tamano_x = 60
        self.tamano_y = 80
        self.speed = 16
        self.dt = 1
        self.boton_x = False
        self.boton_y = False
        self.tiempo_golpe_visual = 0
        self.duracion_golpe_visual = 160
        self.ultima_vida = self.vida
        self.prong = Prongs(mapa)
        self.principal = Principal()
        self.seleccionando_prong = False
        
        # Tamaño visual de cada frame del sprite sheet
        self.sprite_ancho = 70
        self.sprite_alto = 100
        self.animaciones = self.cargar_animaciones()
        # Animación
        self.direccion = "down"
        self.estado = "idle"
        self.frame_actual = 0

        # Milisegundos entre cada frame
        self.velocidad_idle = 400
        self.velocidad_walk = 120
        self.ultimo_cambio_frame = pygame.time.get_ticks()

        #Sonidos
        self.sonido_herido = pygame.mixer.Sound(os.path.join(ruta_actual, "assets", "sounds", "hurt.mp3"))


        self.animaciones = self.cargar_animaciones()

    def input(self,camara):
        keys = pygame.key.get_pressed()

        self.dx = 0
        self.dy = 0

        if keys[pygame.K_a]:
            self.dx = -self.speed
            self.direccion = "left"

        if keys[pygame.K_d]:
            self.dx = self.speed
            self.direccion = "right"

        if keys[pygame.K_w]:
            self.dy = -self.speed
            self.direccion = "up"
            
        if keys[pygame.K_s]:
            self.dy = self.speed
            self.direccion = "down"
            
            
        if self.dx != 0 or self.dy != 0:
            self.estado = "walk"
        else:
            self.estado = "idle"
        # print(len(self.prongs.especiales))

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


        
    def update(self, dt, mapa, camara, enemigos):
        self.tiempo += dt
        self.input(camara)
        self.movimiento(mapa.paredes)
        
        # Actualizar animación
        self.actualizar_animacion(dt)
        
        for prong in self.prong.prongs:
            prong.update(dt, enemigos)
        center = [self.x + self.tamano_x / 2, self.y + self.tamano_y / 2]
        self.principal.update(dt, center, enemigos)
        
        if self.vida < self.ultima_vida:
            self.tiempo_golpe_visual = pygame.time.get_ticks()
            self.sonido_herido.play()

        self.ultima_vida = self.vida

        if self.exp >= self.exp_max:
            self.subirNivel()
    
    def dibujar(self,pantalla,camara):
        frame = self.animaciones[self.direccion][self.frame_actual]

        draw_x = self.x - camara.x
        draw_y = self.y - camara.y - 20
        
        for prong in self.prong.prongs:
            for x in prong.proyectiles:
                pygame.draw.rect(pantalla,"blue",camara.aplicar_rect(x.rectangulo))
                x.dibujar(pantalla, camara) ### Encima para ver si funciona xd
                pygame.draw.rect(pantalla,"blue",camara.aplicar_rect(x[0].rectangulo))

        for x in self.principal.hitbox:
            pygame.draw.rect(pantalla,"blue",camara.aplicar_rect(x.rectangulo))
            
        golpeado = pygame.time.get_ticks() - self.tiempo_golpe_visual < self.duracion_golpe_visual
        
        if golpeado:
            frame = frame.copy()
            
            rojo = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            rojo.fill((255, 0, 0, 90))
            frame.fill((255, 80, 80, 0), special_flags=pygame.BLEND_RGBA_ADD)
            draw_x += random.randint(-4, 4)
            draw_y += random.randint(-4, 4)
            
        pantalla.blit(frame, (int(draw_x), int(draw_y)))
            
    def obtener_tiempo(self):
        minutos = int(self.tiempo) // 60
        segundos = int(self.tiempo) % 60
        
        return f"{minutos:02}:{segundos:02}"
                        
    def cargar_animaciones(self):
        animaciones = {
            "down": [],
            "up": [],
            "left": [],
            "right": []
        }

        hoja = pygame.image.load("assets/images/player_spritesheet.png").convert_alpha()

        frame_ancho = 70
        frame_alto = 100

        columnas = 5

        # Orden de filas de tu sprite sheet
        direcciones = ["down", "up", "left", "right"]

        for fila, direccion in enumerate(direcciones):
            for columna in range(columnas):
                x = columna * frame_ancho
                y = fila * frame_alto

                frame = hoja.subsurface(
                    pygame.Rect(
                        x,
                        y,
                        frame_ancho,
                        frame_alto
                    )
                ).copy()

                animaciones[direccion].append(frame)

        return animaciones
    
    def actualizar_animacion(self, dt):
        tiempo_actual = pygame.time.get_ticks()

        if self.estado == "idle":
            velocidad_actual = self.velocidad_idle
            total_frames = 2   # Solo usa frame 0 y 1
        else:
            velocidad_actual = self.velocidad_walk
            total_frames = 5   # Usa frame 0, 1, 2, 3, 4

        if tiempo_actual - self.ultimo_cambio_frame >= velocidad_actual:
            self.ultimo_cambio_frame = tiempo_actual
            self.frame_actual += 1

            if self.frame_actual >= total_frames:
                self.frame_actual = 0
            

    def subirNivel(self):
        self.exp %= self.exp_max
        self.exp_max += 20
        self.nivel += 1
        self.seleccionando_prong = True


