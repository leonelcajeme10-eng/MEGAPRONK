import pygame
import random


class Enemy:
    def __init__(self, camara):
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
        self.speed = 120

        # Animación
        self.direccion = "down"
        self.frame_actual = 0
        self.tiempo_animacion = 0
        self.velocidad_animacion = 0.12

        self.columnas = 4
        self.filas = 4
        self.escala = 1

        self.animaciones = None

        self.aparicion_enemigos(camara)

    def configurar_sprite(self, ruta, columnas=4, filas=4, escala=1, speed=None, vida=None):
        self.columnas = columnas
        self.filas = filas
        self.escala = escala

        self.animaciones = self.cargar_animaciones(
            ruta,
            self.columnas,
            self.filas,
            self.escala
        )

        frame_inicial = self.animaciones[self.direccion][0]
        self.tamano_x = frame_inicial.get_width()
        self.tamano_y = frame_inicial.get_height()

        self.frame_actual = 0
        self.tiempo_animacion = 0

        if speed is not None:
            self.speed = speed

        if vida is not None:
            self.vida = vida

    def aparicion_enemigos(self, camara):
        borde_izq = camara.x
        borde_derecha = camara.x + camara.ancho
        borde_arriba = camara.y
        borde_abajo = camara.y + camara.alto

        lado = random.choice(["izq", "dere", "arriba", "abajo"])

        if lado == "izq":
            self.x = borde_izq - 100
            self.y = random.randint(int(borde_arriba), int(borde_abajo))

        elif lado == "dere":
            self.x = borde_derecha + 100
            self.y = random.randint(int(borde_arriba), int(borde_abajo))

        elif lado == "arriba":
            self.y = borde_arriba - 100
            self.x = random.randint(int(borde_izq), int(borde_derecha))

        elif lado == "abajo":
            self.y = borde_abajo + 100
            self.x = random.randint(int(borde_izq), int(borde_derecha))

    def movimiento(self, jugador, dt, mapa_rect):
        self.dx = jugador.x - self.x
        self.dy = jugador.y - self.y

        distancia = (self.dx ** 2 + self.dy ** 2) ** 0.5

        if distancia != 0:
            self.dx /= distancia
            self.dy /= distancia

        # Elegir dirección para la animación
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

    def colisiones(self, mapa_rect):
        enemigo_rect = pygame.Rect(
            self.x,
            self.y,
            self.tamano_x,
            self.tamano_y
        )

        if self.boton_x:
            self.boton_x = False

            for pared in mapa_rect:
                if enemigo_rect.colliderect(pared):
                    if self.dx > 0:
                        self.x = pared.left - self.tamano_x
                    elif self.dx < 0:
                        self.x = pared.right

        if self.boton_y:
            self.boton_y = False

            for pared in mapa_rect:
                if enemigo_rect.colliderect(pared):
                    if self.dy > 0:
                        self.y = pared.top - self.tamano_y
                    elif self.dy < 0:
                        self.y = pared.bottom

    def cooldown_golpe(self, jugador):
        enemigo_rect = pygame.Rect(
            self.x,
            self.y,
            self.tamano_x,
            self.tamano_y
        )

        jugador_rect = pygame.Rect(
            jugador.x,
            jugador.y,
            jugador.tamano_x,
            jugador.tamano_y
        )

        if self.inmunidad > 0:
            self.inmunidad -= 1

        if jugador_rect.colliderect(enemigo_rect) and self.inmunidad <= 0:
            self.inmunidad = 60
            jugador.vida -= 10

    def cargar_animaciones(self, ruta, columnas, filas, escala):
        sheet = pygame.image.load(ruta).convert_alpha()

        ancho_frame = sheet.get_width() // columnas
        alto_frame = sheet.get_height() // filas

        animaciones = {
            "up": [],
            "down": [],
            "left": [],
            "right": []
        }

        # Cambia este orden si tu spritesheet usa otro orden de filas
        orden_filas = ["up", "down", "left", "right"]

        for fila in range(filas):
            direccion = orden_filas[fila]

            for columna in range(columnas):
                x = columna * ancho_frame
                y = fila * alto_frame

                frame = sheet.subsurface(
                    pygame.Rect(x, y, ancho_frame, alto_frame)
                ).copy()

                frame = pygame.transform.scale(
                    frame,
                    (
                        ancho_frame * escala,
                        alto_frame * escala
                    )
                )

                animaciones[direccion].append(frame)

        return animaciones

    def animar(self, dt):
        self.tiempo_animacion += dt

        if self.tiempo_animacion >= self.velocidad_animacion:
            self.tiempo_animacion = 0
            self.frame_actual += 1

            if self.frame_actual >= len(self.animaciones[self.direccion]):
                self.frame_actual = 0

    def update(self, jugador, dt, mapa, camara):
        self.movimiento(jugador, dt, mapa.paredes)
        self.cooldown_golpe(jugador)
        self.animar(dt)

    def dibujar(self, pantalla, camara):
        if self.animaciones is None:
            return

        frame = self.animaciones[self.direccion][self.frame_actual]

        pantalla.blit(
            frame,
            (
                self.x - camara.x,
                self.y - camara.y
            )
        )


TIPOS_ENEMIGO = [
    {
        "ruta": "assets/images/ghost_spritesheet.png",
        "columnas": 4,
        "filas": 4,
        "escala": 1,
        "speed": 120,
        "vida": 100
    },
    {
        "ruta": "assets/images/bfly_spritesheet.png",
        "columnas": 4,
        "filas": 4,
        "escala": 1,
        "speed": 90,
        "vida": 120
    }
]


def crear_enemigo(camara):
    enemigo = Enemy(camara)

    datos = random.choice(TIPOS_ENEMIGO)

    enemigo.configurar_sprite(
        datos["ruta"],
        columnas=datos["columnas"],
        filas=datos["filas"],
        escala=datos["escala"],
        speed=datos["speed"],
        vida=datos["vida"]
    )

    return enemigo