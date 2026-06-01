import pygame


CACHE_SPRITES = {}


def cargar_spritesheet(ruta, columnas=4, filas=4, escala=1, orden_filas=None):
    if orden_filas is None:
        orden_filas = ["up", "down", "left", "right"]

    clave = (ruta, columnas, filas, escala, tuple(orden_filas))

    if clave in CACHE_SPRITES:
        return CACHE_SPRITES[clave]

    sheet = pygame.image.load(ruta).convert_alpha()

    ancho_frame = sheet.get_width() // columnas
    alto_frame = sheet.get_height() // filas

    animaciones = {}

    for fila in range(filas):
        direccion = orden_filas[fila]
        animaciones[direccion] = []

        for columna in range(columnas):
            x = columna * ancho_frame
            y = fila * alto_frame

            frame = sheet.subsurface(
                pygame.Rect(x, y, ancho_frame, alto_frame)
            ).copy()

            if escala != 1:
                frame = pygame.transform.scale(
                    frame,
                    (
                        int(ancho_frame * escala),
                        int(alto_frame * escala)
                    )
                )

            animaciones[direccion].append(frame)

    CACHE_SPRITES[clave] = animaciones

    return animaciones


class AnimadorMovimiento:
    def __init__(self, configuracion):
        self.animaciones = cargar_spritesheet(
            ruta=configuracion["ruta"],
            columnas=configuracion.get("columnas", 4),
            filas=configuracion.get("filas", 4),
            escala=configuracion.get("escala", 1),
            orden_filas=configuracion.get(
                "orden_filas",
                ["up", "down", "left", "right"]
            )
        )

        self.direccion = "down"
        self.frame_actual = 0
        self.tiempo = 0
        self.velocidad = configuracion.get("velocidad", 0.12)

    def set_direccion(self, direccion):
        if direccion in self.animaciones:
            self.direccion = direccion

            if self.frame_actual >= len(self.animaciones[self.direccion]):
                self.frame_actual = 0

    def update(self, dt):
        frames = self.animaciones[self.direccion]

        if len(frames) <= 1:
            return

        self.tiempo += dt

        if self.tiempo >= self.velocidad:
            self.tiempo = 0
            self.frame_actual += 1

            if self.frame_actual >= len(frames):
                self.frame_actual = 0

    def imagen_actual(self):
        return self.animaciones[self.direccion][self.frame_actual]
    

def cargar_spritesheet_horizontal(ruta, columnas=5, escala=1):
        clave = (ruta, columnas, escala, "horizontal")

        if clave in CACHE_SPRITES:
            return CACHE_SPRITES[clave]

        sheet = pygame.image.load(ruta).convert_alpha()

        ancho_frame = sheet.get_width() // columnas
        alto_frame = sheet.get_height()

        frames = []

        for columna in range(columnas):
            x = columna * ancho_frame
            y = 0

            frame = sheet.subsurface(pygame.Rect(x, y, ancho_frame, alto_frame)).copy()

            if escala != 1:
                frame = pygame.transform.scale(
                    frame,
                    (
                        int(ancho_frame * escala),
                        int(alto_frame * escala)
                    )
                )

            frames.append(frame)

        CACHE_SPRITES[clave] = frames

        return frames
    
class AnimadorHorizontal:
    def __init__(self, ruta, columnas=5, escala=1, velocidad_ms=80, loop=True):
        self.frames = cargar_spritesheet_horizontal(ruta, columnas, escala)

        self.frame_actual = 0
        self.velocidad_ms = velocidad_ms
        self.loop = loop
        self.terminada = False
        self.ultimo_cambio = pygame.time.get_ticks()

    def update(self):
        if self.terminada:
            return

        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_cambio >= self.velocidad_ms:
            self.ultimo_cambio = tiempo_actual
            self.frame_actual += 1

            if self.frame_actual >= len(self.frames):
                if self.loop:
                    self.frame_actual = 0
                else:
                    self.frame_actual = len(self.frames) - 1
                    self.terminada = True

    def imagen_actual(self):
        return self.frames[self.frame_actual]
    
    
class AnimadorSlash:
    def __init__(self, ruta, columnas=3, filas=4, escala=1, orden_filas=None):
        if orden_filas is None:
            orden_filas = ["down", "up", "left", "right"]

        self.animaciones = cargar_spritesheet(ruta=ruta,columnas=columnas,filas=filas,escala=escala,orden_filas=orden_filas)

    def obtener_frame(self, direccion, fase):
        if direccion not in self.animaciones:
            direccion = "down"

        frames = self.animaciones[direccion]

        if fase < 0:
            fase = 0

        if fase >= len(frames):
            fase = len(frames) - 1

        return frames[fase]
    
class AnimacionMuerte:
    def __init__(self, ancho, alto, duracion=1.5):
        self.ancho = ancho
        self.alto = alto
        self.duracion = duracion
        self.tiempo = 0
        self.activa = False

    def iniciar(self):
        self.tiempo = 0
        self.activa = True

    def actualizar_y_dibujar(self, pantalla, dt, mapa, camara, jugador, enemigos, ui):
        self.tiempo += dt

        pantalla.fill((255, 255, 255))
        mapa.update(pantalla, camara)
        jugador.dibujar(pantalla, camara)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla, camara)

        ui.dibujar_hud(pantalla, jugador)

        progreso = min(self.tiempo / self.duracion, 1)

        overlay = pygame.Surface((self.ancho, self.alto))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(int(255 * progreso))
        pantalla.blit(overlay, (0, 0))

        return self.tiempo >= self.duracion