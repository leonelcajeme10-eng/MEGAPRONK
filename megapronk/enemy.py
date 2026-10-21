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

        def __init__(self, camara, nivel_dificultad=0, es_elite=False):
            self.x = 50
            self.y = 50
            self.dx = 0
            self.dy = 0
            self.nivel_dificultad = nivel_dificultad
            self.es_elite = es_elite

            self.tamano_x = self.TAMANO_X
            self.tamano_y = self.TAMANO_Y

            multiplicador_vida = 1 + 0.12 * nivel_dificultad
            multiplicador_damage = 1 + 0.08 * nivel_dificultad
            multiplicador_speed = min(1.5, 1 + 0.03 * nivel_dificultad)

            self.vida_max = max(1, round(self.VIDA * multiplicador_vida))
            self.vida = self.vida_max
            self.speed = self.SPEED * multiplicador_speed
            self.damage = max(1, round(self.DAMAGE * multiplicador_damage))
            self.color = self.COLOR
            self.experiencia = max(1, round(self.EXP * (1 + 0.05 * nivel_dificultad)))

            self.inmunidad = 60
            self.boton_x = False
            self.boton_y = False
            self.tiempo_golpe_visual = 0
            self.duracion_golpe_visual = 160
            self.fin_carga_elite = 0
            self.proxima_carga_elite = 0
            self.font_elite = None
            

            # Animación
            self.direccion = "down"
            self.animador = None

            if self.ANIMACION_MOVIMIENTO is not None:
                self.animador = AnimadorMovimiento(self.ANIMACION_MOVIMIENTO)

                imagen = self.animador.imagen_actual()
                self.tamano_x = imagen.get_width()
                self.tamano_y = imagen.get_height()

            if self.es_elite:
                self.vida_max = round(self.vida_max * 2.5)
                self.vida = self.vida_max
                self.damage = max(1, round(self.damage * 1.5))
                self.speed *= 1.10
                self.experiencia *= 4
                self.tamano_x = round(self.tamano_x * 1.25)
                self.tamano_y = round(self.tamano_y * 1.25)
                self.font_elite = pygame.font.SysFont("Arial", 14, bold=True)
                self.proxima_carga_elite = pygame.time.get_ticks() + random.randint(2200, 3600)

            self.ultima_vida = self.vida
            
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
            velocidad = self.velocidad_actual()
            mov_x = self.dx * velocidad * dt
            mov_y = self.dy * velocidad * dt
            
            if mov_x != 0:
                self.x += mov_x
                self.boton_x = True
                self.colisiones(mapa_rect)

            if mov_y != 0:
                self.y += mov_y
                self.boton_y = True
                self.colisiones(mapa_rect)

        def velocidad_actual(self):
            if not self.es_elite:
                return self.speed

            ahora = pygame.time.get_ticks()
            if ahora >= self.proxima_carga_elite:
                self.fin_carga_elite = ahora + 650
                self.proxima_carga_elite = ahora + random.randint(3800, 5200)

            if ahora < self.fin_carga_elite:
                return self.speed * 1.65

            return self.speed

        def esta_cargando(self):
            return self.es_elite and pygame.time.get_ticks() < self.fin_carga_elite
            

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

            if self.es_elite:
                self.dibujar_aura_elite(pantalla, draw_x, draw_y)

            if self.animador is not None:
                frame = self.animador.imagen_actual()
                if golpeado:
                    frame = frame.copy()
                    frame.fill((255, 80, 80, 0), special_flags=pygame.BLEND_RGBA_ADD)

                if self.es_elite:
                    frame = pygame.transform.smoothscale(
                        frame,
                        (int(self.tamano_x), int(self.tamano_y)),
                    )

                pantalla.blit(frame, (draw_x, draw_y))
                if self.es_elite:
                    self.dibujar_barra_elite(pantalla, draw_x, draw_y)
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

            if self.es_elite:
                self.dibujar_barra_elite(pantalla, draw_x, draw_y)

        def dibujar_aura_elite(self, pantalla, draw_x, draw_y):
            radio = max(28, int(max(self.tamano_x, self.tamano_y) * 0.75))
            aura = pygame.Surface((radio * 2, radio * 2), pygame.SRCALPHA)
            color = (255, 100, 45, 150) if self.esta_cargando() else (185, 80, 255, 110)
            pygame.draw.circle(aura, color, (radio, radio), radio - 3, 4)

            centro = (
                int(draw_x + self.tamano_x / 2),
                int(draw_y + self.tamano_y / 2),
            )
            pantalla.blit(aura, (centro[0] - radio, centro[1] - radio))

        def dibujar_barra_elite(self, pantalla, draw_x, draw_y):
            ancho = max(55, int(self.tamano_x))
            alto = 7
            x = int(draw_x + self.tamano_x / 2 - ancho / 2)
            y = int(draw_y - 16)
            porcentaje = max(0, min(1, self.vida / self.vida_max))

            pygame.draw.rect(pantalla, (20, 10, 25), (x, y, ancho, alto))
            pygame.draw.rect(pantalla, (190, 65, 230), (x, y, int(ancho * porcentaje), alto))
            pygame.draw.rect(pantalla, (255, 210, 255), (x, y, ancho, alto), 1)

            texto = self.font_elite.render("ELITE", True, (255, 225, 255))
            pantalla.blit(texto, texto.get_rect(center=(x + ancho // 2, y - 8)))

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
