import pygame
import random
import os
ruta_actual = os.path.dirname(__file__)

class PauseMenu:
    def __init__(self, ancho, alto, control=None):
        self.control = control
        self.ancho = ancho
        self.alto = alto
        self.pausado = False
        self.font_titulo = pygame.font.SysFont("Georgia", 90)
        self.font_boton = pygame.font.SysFont("Georgia", 45)
        self.botones = {
            "continuar": pygame.Rect(ancho//2 - 250, alto//2 - 30, 500, 80),
            "salir": pygame.Rect(ancho//2 - 250, alto//2 + 90, 500, 80)
        }
        self.opciones = list(self.botones)
        self.indice_seleccionado = 0
        self.borde_menu = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "borde_pausa.png"))
        self.borde_menu = pygame.transform.smoothscale(self.borde_menu, (925,575))
        self.volumen = 0.8
        self.arrastrando_volumen = False
        self.barra_volumen = pygame.Rect(ancho - 260,alto - 60,200,10)
        self.particulas = []

        for i in range(80):
            self.particulas.append([
                random.randint(0, ancho),
                random.randint(0, alto),
                random.randint(2, 5),
                random.uniform(20, 70)
            ])

    def manejar_evento(self, evento):
        accion_control = (
            self.control.accion_menu(evento) if self.control is not None else None
        )
        if accion_control == "pausa":
            self.pausado = not self.pausado
        elif self.pausado and accion_control == "arriba":
            self.indice_seleccionado = (
                self.indice_seleccionado - 1
            ) % len(self.opciones)
        elif self.pausado and accion_control == "abajo":
            self.indice_seleccionado = (
                self.indice_seleccionado + 1
            ) % len(self.opciones)
        elif self.pausado and accion_control == "izquierda":
            self.volumen = max(0, self.volumen - 0.05)
        elif self.pausado and accion_control == "derecha":
            self.volumen = min(1, self.volumen + 0.05)
        elif self.pausado and accion_control == "aceptar":
            opcion = self.opciones[self.indice_seleccionado]
            if opcion == "continuar":
                self.pausado = False
            else:
                return "salir"
        elif self.pausado and accion_control == "cancelar":
            self.pausado = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.pausado = not self.pausado

            elif self.pausado and evento.key in (pygame.K_w, pygame.K_UP):
                self.indice_seleccionado = (
                    self.indice_seleccionado - 1
                ) % len(self.opciones)
            elif self.pausado and evento.key in (pygame.K_s, pygame.K_DOWN):
                self.indice_seleccionado = (
                    self.indice_seleccionado + 1
                ) % len(self.opciones)
            elif self.pausado and evento.key in (pygame.K_a, pygame.K_LEFT):
                self.volumen = max(0, self.volumen - 0.05)
            elif self.pausado and evento.key in (pygame.K_d, pygame.K_RIGHT):
                self.volumen = min(1, self.volumen + 0.05)
            elif self.pausado and evento.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER,
                pygame.K_SPACE,
            ):
                opcion = self.opciones[self.indice_seleccionado]
                if opcion == "continuar":
                    self.pausado = False
                else:
                    return "salir"

        if self.pausado and evento.type == pygame.MOUSEBUTTONDOWN:
            mouse = evento.pos

            if self.botones["continuar"].collidepoint(mouse):
                self.indice_seleccionado = self.opciones.index("continuar")
                self.pausado = False

            if self.botones["salir"].collidepoint(mouse):
                self.indice_seleccionado = self.opciones.index("salir")
                return "salir"

            if self.barra_volumen.collidepoint(evento.pos):
                self.arrastrando_volumen = True

        if self.pausado and evento.type == pygame.MOUSEBUTTONUP:
            self.arrastrando_volumen = False

        if self.pausado and evento.type == pygame.MOUSEMOTION and self.arrastrando_volumen:
            mouse_x = evento.pos[0]
            self.volumen = (mouse_x - self.barra_volumen.x) / self.barra_volumen.width
            self.volumen = max(0, min(1, self.volumen))

        if self.pausado and evento.type == pygame.MOUSEMOTION:
            for indice, opcion in enumerate(self.opciones):
                if self.botones[opcion].collidepoint(evento.pos):
                    self.indice_seleccionado = indice
                    break
        
        pygame.mixer.music.set_volume(self.volumen)

        return None

    def actualizar(self, dt):
        if not self.pausado:
            return

        for p in self.particulas:
            p[1] -= p[3] * dt

            if p[1] < -10:
                p[0] = random.randint(0, self.ancho)
                p[1] = self.alto + 10

    def dibujar_fondo_difuminado(self, pantalla):
        copia = pantalla.copy()

        pequeño = pygame.transform.smoothscale(copia, (self.ancho // 12, self.alto // 12))
        blur = pygame.transform.smoothscale(pequeño, (self.ancho, self.alto))

        pantalla.blit(blur, (0, 0))

        oscuro = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        oscuro.fill((0, 0, 0, 120))
        pantalla.blit(oscuro, (0, 0))

    def dibujar_particulas(self, pantalla):
        for x, y, radio, velocidad in self.particulas:
            pygame.draw.circle(pantalla,(212, 175, 55), (int(x), int(y)), radio)

    def dibujar_boton(self, pantalla, rect, texto, seleccionado=False):
        mouse = pygame.mouse.get_pos()
        activo = seleccionado or rect.collidepoint(mouse)

        color_fondo = (55, 40, 20) if seleccionado else (25, 20, 15)
        color_borde = (255, 210, 80) if activo else (160, 120, 40)

        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)
        pygame.draw.rect(pantalla, color_borde, rect, width=4, border_radius=12)

        render = self.font_boton.render(texto, True, (255, 240, 200))
        pantalla.blit(render, (rect.centerx - render.get_width() // 2, rect.centery - render.get_height() // 2))

    def dibujar(self, pantalla):
        if not self.pausado:
            return

        self.dibujar_fondo_difuminado(pantalla)
        self.dibujar_particulas(pantalla)

        # Marco grande
        borde_x = self.ancho // 2 - 452
        borde_y = self.alto // 2 - 300

        # Cuadro negro interno
        menu = pygame.Rect(
        self.ancho // 2 - 407,
        self.alto // 2 - 258,835, 491)

        pygame.draw.rect(pantalla, (10, 8, 8), menu, border_radius=18)

        pantalla.blit(self.borde_menu, (borde_x, borde_y))

        titulo = self.font_titulo.render("PAUSA", True, (212, 175, 55))
        pantalla.blit(titulo, (menu.centerx - titulo.get_width() // 2,menu.y + 45))

        for indice, opcion in enumerate(self.opciones):
            self.dibujar_boton(
                pantalla,
                self.botones[opcion],
                opcion.upper(),
                indice == self.indice_seleccionado,
            )
        
        icono = self.font_boton.render("♪", True, (255, 210, 80))
        pantalla.blit(icono, (self.ancho - 180, self.alto - 115))
        texto_vol = self.font_boton.render(
            f"{int(self.volumen * 100)}%",
            True,
            (255, 240, 200)
        )

        pantalla.blit(
            texto_vol,
            (self.ancho - 360, self.alto - 85)
        )

        pygame.draw.rect(
            pantalla,
            (40, 30, 20),
            self.barra_volumen,
            border_radius=5
        )

        pygame.draw.rect(
            pantalla,
            (255, 210, 80),
            (
                self.barra_volumen.x,
                self.barra_volumen.y,
                int(self.barra_volumen.width * self.volumen),
                self.barra_volumen.height
            ),
            border_radius=5
        )

        pygame.draw.circle(
            pantalla,
            (255, 240, 200),
            (
                self.barra_volumen.x +
                int(self.barra_volumen.width * self.volumen),
                self.barra_volumen.centery
            ),
            10
        )
