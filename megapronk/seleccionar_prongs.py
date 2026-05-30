import pygame
import random
import os
import math
import player
ruta_actual = os.path.dirname(__file__)
from prong import Prong, BolaFuego, ProngBomba
from modificadores import damageAumento, disminuirCooldown

class SeleccionarProngs:
    def __init__(self, jugador):
        self.opciones = []
        self.activo = False
        self.cartas = []
        self.font_titulo = pygame.font.SysFont("Georgia", 60)
        self.font_texto = pygame.font.SysFont("Georgia", 32)
        self.ancho = 1920
        self.alto = 1080
        self.cont = 0
        self.slot_actual = 0
        self.teclas = [pygame.K_1, pygame.K_2, pygame.K_3]
        self.tecla = self.teclas[self.slot_actual]
        self.jugador = jugador
        self.bancoOpciones = [OpcionProng(BolaFuego, self.jugador, "Bola De fuego", "agrega prong"), OpcionProng(Prong, self.jugador, "Flecha", "agrega prong"), OpcionProng(ProngBomba, self.jugador, "Bomba", "agrega prong")]
        self.opciones = [self.bancoOpciones[0], self.bancoOpciones[1], self.bancoOpciones[2]]

    def abrir(self):
        self.activo = True

    def cerrar(self):
        self.activo = False
        
    def manejar_evento(self, evento):
        if not self.activo:
            return None
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            tecla_presionada = self.teclas[self.slot_actual] 
            
            for i, rect in enumerate(self.cartas):
                if rect.collidepoint(mouse):
                    if isinstance(self.opciones[i], OpcionProng):

                        especial = self.opciones[i].ejecutar(tecla_presionada)
                        
                        self.agregarOpciones(especial, self.opciones[i].nombre)
                        self.bancoOpciones.remove(self.opciones[i])
                        self.slot_actual += 1 if self.slot_actual < 2 else 0
                    else:
                        self.opciones[i].ejecutar()
                        if self.opciones[i].descripcion == "disminuye cooldown":
                            if self.opciones[i].especial.cooldown_time <= 1:
                                self.bancoOpciones.remove(self.opciones[i])
                                                 
                    self.asignarOpciones()
                    self.cerrar()
                    return

    def dibujar(self, pantalla):
        if not self.activo:
            return

        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        pantalla.blit(overlay, (0, 0))

        titulo = self.font_titulo.render("Selecciona una carta", True, (230, 200, 120))
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 180)))

        self.cartas = []

        x_inicial = self.ancho // 2 - 480
        y = 320

        for i, opcion in enumerate(self.opciones):
            rect = pygame.Rect(x_inicial + i * 340, y, 280, 380)
            self.cartas.append(rect)

            nombre = opcion.nombre
            descripcion = opcion.descripcion

            pygame.draw.rect(pantalla, (20, 18, 30), rect, border_radius=25)
            pygame.draw.rect(pantalla, (210, 160, 60), rect, 4, border_radius=25)

            texto = self.font_texto.render(nombre, True, (255, 240, 180))
            pantalla.blit(texto, texto.get_rect(center=(rect.centerx, rect.centery)))
            texto = self.font_texto.render(descripcion, True, (255, 240, 180))
            pantalla.blit(texto, texto.get_rect(center=(rect.centerx, rect.centery - 100)))

    def agregarOpciones(self, especial, nombre):
        self.bancoOpciones.append(opcionModificador(especial, damageAumento, 20, nombre, "aumenta daño"))
        self.bancoOpciones.append(opcionModificador(especial, disminuirCooldown, 0.5, nombre, "disminuye cooldown"))

    def asignarOpciones(self):
        self.opciones.clear()
        numeros = random.sample(range(0, len(self.bancoOpciones)), 3)

        for i, opcion in enumerate(numeros):
            self.opciones.append(self.bancoOpciones[opcion])
        

class OpcionProng:
    def __init__(self, prong, jugador, nombre, descripcion):
        self.prong = prong  
        self.jugador = jugador
        self.nombre = nombre
        self.descripcion = descripcion

    def ejecutar(self, tecla_actual):
        return self.jugador.agregarProng(tecla_actual, self.prong)

class opcionModificador:
    def __init__(self, especial, funcion, aumento, nombre, descripcion):
        self.especial = especial
        self.funcion = funcion 
        self.aumento = aumento
        self.nombre = nombre
        self.descripcion = descripcion

    def ejecutar(self):
        self.funcion(self.especial , self.especial.Prong, self.aumento)
        