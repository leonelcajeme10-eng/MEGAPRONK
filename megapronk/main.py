import pygame
from player import Player
from enemy import Enemy
from mapa import Mapa
from camara import Camara
from prong import Prong, BolaFuego, ProngBomba
from ui import UI
from pausa import PauseMenu
from audio import cargar_sonidos
from menu import Menu
import os 
ruta_actual = os.path.dirname(__file__)
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
from enemigo_mariposa import Mariposa
from fantasma import Fantasma,Proyectil_enemigo
from seleccionar_prongs import SeleccionarProngs
from pantalla_final import PantallaFinal
from anim import AnimacionMuerte
from controles import Control
from dificultad import DirectorDificultad

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
pantalla = pygame.display.set_mode((1920,1080))
control = Control()
pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "menu.ogg"))
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

pygame.display.set_caption("Megapronk")

mapa = Mapa()
jugador = Player(mapa, control)
camara = Camara()
ui = UI()
pantalla_final = PantallaFinal(1920, 1080, control)
tiempo_spawn = 0
enemigos = []
pause = PauseMenu(1920, 1080, control)
menu = Menu(1920, 1080, control)
estado = "menu"
proyectiles = []
cargar_sonidos(ruta_actual)
tiempo_de_fantasma = 0
director_dificultad = DirectorDificultad()
ejecutando = True
musica_megapronk = False 
animacion_muerte = AnimacionMuerte(1920, 1080)
pause.volumen = menu.volumen
tiempo_aumento = 10.0

while ejecutando:
    accion = None
    for evento in pygame.event.get():
        control.procesar_evento(evento)

        if evento.type == pygame.QUIT:
            ejecutando = False

        if estado == "menu":
            accion = menu.manejar_evento(evento)

            if accion == "jugar":
                pause.volumen = menu.volumen
                jugador = Player(mapa, control)
                camara = Camara()
                enemigos = []
                proyectiles = []
                tiempo_spawn = 0
                tiempo_de_fantasma = 0
                director_dificultad = DirectorDificultad()
                pause.pausado = False
                seleccion = SeleccionarProngs(jugador, control)
                estado = "juego"
                pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "gameplay.ogg"))
                pygame.mixer.music.play(-1)    

            elif accion == "salir":
                ejecutando = False

        elif estado == "juego":
            accion = pause.manejar_evento(evento)

            if accion == "salir":
                menu.volumen = pause.volumen
                estado = "menu"
                pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "menu.ogg"))
                pygame.mixer.music.play(-1)
                
        elif estado == "seleccion":
            seleccion.manejar_evento(evento)

            if not seleccion.activo:
                estado = "juego"
                        
        elif estado == "final":
            accion = pantalla_final.manejar_evento(evento)

            if accion == "salir":
                menu.volumen = pause.volumen
                estado = "menu"
                pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "menu.ogg"))
                pygame.mixer.music.play(-1)
            
    dt = clock.tick(60) / 1000.0

    pause.actualizar(dt)

    if estado == "juego" and jugador.vida <= 0:
        estado = "muriendo"
        animacion_muerte.iniciar()

    if estado == "muriendo":
        terminada = animacion_muerte.actualizar_y_dibujar(
            pantalla, dt, mapa, camara, jugador, enemigos, ui
        )

        pygame.display.flip()

        if terminada:
            estado = "final"
            pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "final.ogg"))
            pygame.mixer.music.play(-1)

        continue
    
    if estado == "juego":
        if jugador.megapronkBandera and not musica_megapronk:
            pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "megapronk.ogg"))
            pygame.mixer.music.play(-1)
            musica_megapronk = True
        elif not jugador.megapronkBandera and musica_megapronk:
            pygame.mixer.music.load(os.path.join(ruta_actual, "assets", "music", "gameplay.ogg"))
            pygame.mixer.music.play(-1)
            musica_megapronk = False
    
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
    tiempo_de_fantasma += dt
    nivel_dificultad = director_dificultad.nivel(jugador.tiempo)

    if tiempo_spawn >= director_dificultad.intervalo_mariposa(nivel_dificultad):
        if director_dificultad.puede_generar(len(enemigos), nivel_dificultad):
            es_elite = director_dificultad.debe_generar_elite(
                jugador.tiempo,
                enemigos,
                nivel_dificultad,
            )
            enemigos.append(Mariposa(camara, nivel_dificultad, es_elite))
        tiempo_spawn = 0
    if tiempo_de_fantasma >= director_dificultad.intervalo_fantasma(nivel_dificultad):
        if director_dificultad.puede_generar(len(enemigos), nivel_dificultad):
            es_elite = director_dificultad.debe_generar_elite(
                jugador.tiempo,
                enemigos,
                nivel_dificultad,
            )
            enemigos.append(Fantasma(camara, nivel_dificultad, es_elite))
        tiempo_de_fantasma = 0


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


