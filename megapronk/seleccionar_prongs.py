import pygame
import random
import os
import math
import player
ruta_actual = os.path.dirname(__file__)
from prong import Prong, BolaFuego, ProngBomba
from modificadores import damageAumento, disminuirCooldown, aumentarVelocidad, damageAumentoSet, aumentoCritSet, aumentoCrit, aumentoProbCrit, aumentoProbCritSet

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
<<<<<<< Updated upstream
        self.teclas = [pygame.K_1, pygame.K_2, pygame.K_3]
        self.tecla = self.teclas[self.slot_actual]
        self.jugador = jugador
        self.bancoOpciones = self.crearBanco()
        self.opciones = [self.bancoOpciones[0], self.bancoOpciones[1], self.bancoOpciones[2]]

    def crearBanco(self):
        banco = []
        banco.append(OpcionProng(BolaFuego, self.jugador, "Bola De fuego", "agrega prong"))
        banco.append(OpcionProng(Prong, self.jugador, "Flecha", "agrega prong"))
        banco.append(OpcionProng(ProngBomba, self.jugador, "Bomba", "agrega prong"))
        banco.append(opcionJugador(self.jugador, aumentarVelocidad, 2, "Jugador", "Aumentar Velocidad"))
        banco.append(OpcionSet(self.jugador.principal, damageAumentoSet, 10, "Ataque Principal", "Aumentar Daño"))
        banco.append(OpcionSet(self.jugador.principal, aumentoProbCritSet, 5, "Ataque Principal", "Probabilidad Crit"))
        banco.append(OpcionSet(self.jugador.principal, aumentoCritSet, 0.2, "Ataque Principal", "Daño Crit"))
        return banco

    def abrir(self):
        self.activo = True
=======
        self.teclas = [pygame.K_1, pygame.K_2, pygame.K_3]
        self.tecla = self.teclas[self.slot_actual]
        self.jugador = jugador
        self.tiempo_apertura = pygame.time.get_ticks()
        self.marco_carta = pygame.image.load(os.path.join(ruta_actual, "assets", "ui", "borde_pausa.png"))
        self.marco_carta = pygame.transform.smoothscale(self.marco_carta, (400,520))
        self.danio = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "danio.png"))
        self.danio = pygame.transform.smoothscale(self.danio, (140,140))
        self.velocidad = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "velocidad.png"))
        self.velocidad = pygame.transform.smoothscale(self.velocidad, (140,140))        
        self.cooldown = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "cooldown.png"))
        self.cooldown = pygame.transform.smoothscale(self.cooldown, (140,140))     
        self.critico = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "critico.png"))
        self.critico = pygame.transform.smoothscale(self.critico, (140,140))  
        self.danio_critico = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "danio_critico.png"))
        self.danio_critico = pygame.transform.smoothscale(self.danio_critico, (140,140))        
        self.bancoOpciones = self.crearBanco()
        self.opciones = [self.bancoOpciones[0], self.bancoOpciones[1], self.bancoOpciones[2]]

    def crearBanco(self):
        banco = []
        banco.append(OpcionProng(BolaFuego, self.jugador, "Bola De fuego", "Nueva Habilidad"))
        banco.append(OpcionProng(Prong, self.jugador, "Flecha", "Nueva Habilidad"))
        banco.append(OpcionProng(ProngBomba, self.jugador, "Bomba", "Nueva Habilidad"))
        banco.append(opcionJugador(self.jugador, aumentarVelocidad, 2, "Jugador", "Aumentar Velocidad", self.jugador.icono, self.velocidad))
        banco.append(OpcionSet(self.jugador.principal, damageAumentoSet, 10, "Ataque Principal", "Aumentar Daño", self.jugador.icono, self.danio))
        banco.append(OpcionSet(self.jugador.principal, aumentoProbCritSet, 5, "Ataque Principal", "Probabilidad Crit", self.jugador.icono, self.critico))
        banco.append(OpcionSet(self.jugador.principal, aumentoCritSet, 0.2, "Ataque Principal", "Daño Crit", self.jugador.icono, self.danio_critico))
        return banco

    def abrir(self):
        self.activo = True
        self.tiempo_apertura = pygame.time.get_ticks()
>>>>>>> Stashed changes

    def cerrar(self):
        self.activo = False
        
    def manejar_evento(self, evento):
        if not self.activo:
            return None
        
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.tiempo_apertura < 300:
            return
        
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

                    elif isinstance(self.opciones[i], opcionModificador):
                        self.opciones[i].ejecutar()
                        if self.opciones[i].descripcion == "disminuye cooldown":
                            if self.opciones[i].especial.cooldown_time <= 1:
                                self.bancoOpciones.remove(self.opciones[i])
                        elif self.opciones[i].descripcion =="Probabilidad Crit":
                            if self.opciones[i].especial.Prong.probCrit >= 100:
                                self.bancoOpciones.remove(self.opciones[i])

                    elif isinstance(self.opciones[i], opcionJugador):
                        self.opciones[i].ejecutar()
                        if self.opciones[i].descripcion == "Aumentar Velocidad":
                            if self.jugador.speed >= 20:
                                self.bancoOpciones.remove(self.opciones[i])

                    elif isinstance(self.opciones[i], OpcionSet):
                        self.opciones[i].ejecutar()
                        if self.opciones[i].descripcion =="Probabilidad Crit":
                            if self.opciones[i].principal.set.probCrit >= 100:
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

<<<<<<< Updated upstream
        titulo = self.font_titulo.render("Selecciona una carta", True, (230, 200, 120))
=======
        titulo = self.font_titulo.render("Selecciona un Pronk", True, (230, 200, 120))
>>>>>>> Stashed changes
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, 180)))

        self.cartas = []

        x_inicial = self.ancho // 2 - 575
        y = 320

<<<<<<< Updated upstream
        for i, nombre in enumerate(self.opciones):
            rect = pygame.Rect(x_inicial + i * 340, y, 280, 380)
            self.cartas.append(rect)

            nombre = opcion.nombre
            descripcion = opcion.descripcion

            pygame.draw.rect(pantalla, (20, 18, 30), rect, border_radius=25)
            pygame.draw.rect(pantalla, (210, 160, 60), rect, 4, border_radius=25)

            texto = self.font_texto.render(nombre, True, (255, 240, 180))
            pantalla.blit(texto, texto.get_rect(center=(rect.centerx, rect.centery)))
=======
        for i, opcion in enumerate(self.opciones):
            rect = pygame.Rect(x_inicial + i * 420, y, 400, 500)
            self.cartas.append(rect)
            alineacion_x = rect.centerx - 15
            nombre = opcion.nombre
            descripcion = opcion.descripcion

            fondo = pygame.Rect(rect.x, rect.y, rect.width - 30, rect.height - 30)

            pygame.draw.rect(pantalla,(10, 8, 8),fondo,border_radius=12)

            pantalla.blit(self.marco_carta,(rect.x - 20, rect.y - 20))
            
            icono_principal = None
            icono_atributo = None
            
            if isinstance(opcion, OpcionProng):
                x_icono = alineacion_x
            else:
                x_icono = alineacion_x - 35
            
            if isinstance(opcion, OpcionProng):
                icono_principal = opcion.prong.icono
            elif isinstance(opcion, opcionJugador):
                icono_principal = opcion.jugador.icono
                icono_atributo = opcion.icono_atributo
            elif isinstance(opcion, opcionModificador):
                icono_principal = opcion.especial.Prong.icono
                icono_atributo = opcion.icono
            elif isinstance(opcion, OpcionSet):
                icono_principal = opcion.imagen
                icono_atributo = opcion.atributo
            
            if icono_principal is not None:
                pantalla.blit(icono_principal,icono_principal.get_rect(center=(x_icono, rect.y + 210)))
            
            if icono_atributo is not None:
                pantalla.blit(icono_atributo,icono_atributo.get_rect(center=(alineacion_x+65, rect.y + 250)))

            texto = self.font_texto.render(nombre, True, (255, 240, 180))
            pantalla.blit(texto, texto.get_rect(center=(alineacion_x, rect.centery - 180 )))
            texto = self.font_texto.render(descripcion, True, (255, 240, 180))
            pantalla.blit(texto, texto.get_rect(center=(alineacion_x, rect.centery + 110)))
            
            if hasattr(opcion, "estadistica"):
                texto_stat = self.font_texto.render(opcion.estadistica, True, (180, 255, 180))
                pantalla.blit(texto_stat,texto_stat.get_rect(center=(alineacion_x, rect.centery + 155)))

    def agregarOpciones(self, especial, nombre):
        self.bancoOpciones.append(opcionModificador(especial, damageAumento, 20, nombre, "Aumentar daño", self.danio, "+20 daño"))
        self.bancoOpciones.append(opcionModificador(especial, disminuirCooldown, 0.5, nombre, "Disminuir cooldown", self.cooldown, "0.5s cooldown"))
        self.bancoOpciones.append(opcionModificador(especial, aumentoProbCrit, 5, nombre, "Probabilidad Crit", self.critico, "5% prob. critico"))
        self.bancoOpciones.append(opcionModificador(especial, aumentoCrit, 0.2, nombre, "Daño Crit", self.danio_critico, "20% daño critico"))

    def asignarOpciones(self):
        self.opciones.clear()
        numeros = random.sample(range(0, len(self.bancoOpciones)), 3)

        for i, opcion in enumerate(numeros):
            self.opciones.append(self.bancoOpciones[opcion])

# agregar atributo de imagen y así panita leoneo

class OpcionProng:
    def __init__(self, prong, jugador, nombre, descripcion, imagen=None):
        self.prong = prong  
        self.jugador = jugador
        self.nombre = nombre
        self.descripcion = descripcion
        self.imagen = imagen

    def ejecutar(self, tecla_actual):
        return self.jugador.agregarProng(tecla_actual, self.prong)

class opcionModificador:
    def __init__(self, especial, funcion, aumento, nombre, descripcion, icono=None, estadistica=""):
        self.especial = especial
        self.funcion = funcion 
        self.aumento = aumento
        self.nombre = nombre
        self.descripcion = descripcion
        self.icono = icono
        self.estadistica = estadistica
    def ejecutar(self):
        self.funcion(self.especial , self.especial.Prong, self.aumento)
        self.especial.nivel += 1
        
class opcionJugador:
    def __init__(self, jugador, funcion, aumento, nombre, descripcion, icono=None, icono_atributo=None):
        self.jugador = jugador
        self.funcion = funcion 
        self.aumento = aumento
        self.nombre = nombre
        self.descripcion = descripcion
        self.icono = icono
        self.icono_atributo = icono_atributo

    def ejecutar(self):
        self.funcion(self.jugador, self.aumento)
        self.jugador.nivel_ataque += 1

class OpcionSet:
    def __init__(self, principal, funcion, aumento, nombre, descripcion, imagen=None, atributo=None):
        self.principal = principal
        self.funcion = funcion
        self.aumento = aumento
        self.nombre = nombre
        self.descripcion = descripcion
        self.imagen = imagen
        self.atributo = atributo

    def ejecutar(self):
        self.funcion(self.principal, self.principal.set, self.aumento)
>>>>>>> Stashed changes
