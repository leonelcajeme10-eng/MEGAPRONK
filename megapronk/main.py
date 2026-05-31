import pygame
from player import Player
from enemy import Enemy
from mapa import Mapa
from camara import Camara
from prong import Prong, BolaFuego, ProngBomba
from ui import UI
from pausa import PauseMenu
from menu import Menu
import os 
ruta_actual = os.path.dirname(__file__)
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
from enemigo_mariposa import Mariposa
from fantasma import Fantasma,Proyectil_enemigo
from seleccionar_prongs import SeleccionarProngs
from pantalla_final import PantallaFinal

pygame.init()
pygame.mixer.init()
pantalla = pygame.display.set_mode((1920,1080))
pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "menu.ogg"))
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

mapa = Mapa()
jugador = Player(mapa)
camara = Camara()
ui = UI()
pantalla_final = PantallaFinal(1920, 1080)
tiempo_spawn = 0
enemigos = []
pause = PauseMenu(1920, 1080)
menu = Menu(1920, 1080)
estado = "menu"
proyectiles = []

ejecutando = True

while ejecutando:
    accion = None
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if estado == "menu":
            accion = menu.manejar_evento(evento)

            if accion == "jugar":
                jugador = Player(mapa)
                camara = Camara()
                enemigos = []
                proyectiles = []
                tiempo_spawn = 0
                pause.pausado = False
                seleccion = SeleccionarProngs(jugador)
                estado = "juego"
                pygame.mixer.music.stop()


            elif accion == "salir":
                ejecutando = False

        elif estado == "juego":
            accion = pause.manejar_evento(evento)

            if accion == "salir":
                estado = "menu"
                pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "menu.ogg"))
                pygame.mixer.music.play(-1)
                
            if jugador.vida <= 0:
                estado = "final"
                
        elif estado == "seleccion":
            seleccion.manejar_evento(evento)

            if not seleccion.activo:
                estado = "juego"
                
        elif estado == "final":
            accion = pantalla_final.manejar_evento(evento)

            if accion == "salir":
                estado = "menu"
                pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "menu.ogg"))
                pygame.mixer.music.play(-1)
            
    dt = clock.tick(60) / 1000.0
         
    pause.actualizar(dt)
    
    if estado == "menu":
        menu.actualizar(dt)
        menu.dibujar(pantalla)
        pygame.display.flip()
        continue

    if pause.pausado:
        pantalla.fill((255, 255, 255))
        mapa.update(pantalla, camara)
        jugador.dibujar(pantalla, camara)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla, camara)

        ui.dibujar_hud(pantalla, jugador)
        pause.dibujar(pantalla)

        pygame.display.flip()
        continue
    
    if estado == "seleccion":
        pantalla.fill((255, 255, 255))
        mapa.update(pantalla, camara)
        jugador.dibujar(pantalla, camara)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla, camara)

        ui.dibujar_hud(pantalla, jugador)
        seleccion.dibujar(pantalla)

        pygame.display.flip()
        continue
    
    if estado == "final":
        pantalla_final.actualizar(dt)
        pantalla_final.dibujar(pantalla, jugador)
        pygame.display.flip()
        continue

    tiempo_spawn += dt
    if tiempo_spawn >= 1:
        enemigos.append(Fantasma(camara))
        enemigos.append(Mariposa(camara))
        tiempo_spawn = 0

    jugador.update(dt, mapa, camara, enemigos)
    camara.update(jugador, dt, mapa)
    
    if jugador.seleccionando_prong:
        seleccion.abrir()
        jugador.seleccionando_prong = False
        estado = "seleccion"

    pantalla.fill((255, 255, 255))
    mapa.update(pantalla, camara)
    jugador.dibujar(pantalla, camara)

    for enemigo in enemigos:
        enemigo.update(jugador, dt, mapa, camara,enemigos,proyectiles)
        enemigo.dibujar(pantalla, camara)
    
    for proyectil in proyectiles:
        proyectil.update(mapa,proyectiles,camara,dt,jugador)
        proyectil.dibujar(pantalla,camara)

    ui.dibujar_hud(pantalla, jugador)
    pause.dibujar(pantalla)
    seleccion.dibujar(pantalla)

    pygame.display.flip()
    

pygame.quit()


