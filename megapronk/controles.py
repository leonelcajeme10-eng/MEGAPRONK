import math

import pygame


class Control:
    """Lee un control conectado sin impedir el uso de teclado y mouse."""

    ZONA_MUERTA = 0.22
    UMBRAL_MENU = 0.65

    # Distribución estándar que usan controles Xbox y la mayoría de controles
    # PlayStation a través de SDL.
    BOTON_ACEPTAR = 0       # A / Cross
    BOTON_CANCELAR = 1      # B / Circle
    BOTON_ATAQUE = 0        # A / Cross durante la partida
    BOTONES_ESPECIALES = (2, 3, 1)  # X, Y y B / Square, Triangle y Circle
    BOTON_PAUSA = 7         # Start / Options
    EJE_GATILLO_DERECHO = 5

    def __init__(self):
        self.joystick = None
        self.eje_menu_activo = {"x": False, "y": False}
        self.conectar_disponible()

    def conectar_disponible(self, indice=0):
        """Conecta el primer mando disponible, si aún no hay uno activo."""
        if self.joystick is not None or pygame.joystick.get_count() == 0:
            return

        try:
            self.joystick = pygame.joystick.Joystick(indice)
            self.joystick.init()
            print(f"Control conectado: {self.joystick.get_name()}")
        except pygame.error:
            self.joystick = None

    def procesar_evento(self, evento):
        """Mantiene el control actualizado si se conecta o desconecta."""
        if evento.type == getattr(pygame, "JOYDEVICEADDED", -1):
            self.conectar_disponible(getattr(evento, "device_index", 0))
            return

        if evento.type != getattr(pygame, "JOYDEVICEREMOVED", -1):
            return

        if self.joystick is None:
            return

        id_desconectado = getattr(evento, "instance_id", None)
        if id_desconectado is None or id_desconectado == self.joystick.get_instance_id():
            self.joystick.quit()
            self.joystick = None
            self.eje_menu_activo = {"x": False, "y": False}
            self.conectar_disponible()

    def _eje(self, indice):
        if self.joystick is None:
            return 0.0

        try:
            if indice >= self.joystick.get_numaxes():
                return 0.0
            return self.joystick.get_axis(indice)
        except pygame.error:
            self.joystick = None
            return 0.0

    def _vector_filtrado(self, eje_x, eje_y):
        magnitud = math.hypot(eje_x, eje_y)
        if magnitud <= self.ZONA_MUERTA:
            return 0.0, 0.0

        # Mantiene la dirección y hace gradual la salida de la zona muerta.
        intensidad = min(1.0, (magnitud - self.ZONA_MUERTA) / (1 - self.ZONA_MUERTA))
        return eje_x / magnitud * intensidad, eje_y / magnitud * intensidad

    def movimiento(self):
        """Vector del stick izquierdo."""
        return self._vector_filtrado(self._eje(0), self._eje(1))

    def boton_presionado(self, boton):
        if self.joystick is None:
            return False

        try:
            return boton < self.joystick.get_numbuttons() and bool(
                self.joystick.get_button(boton)
            )
        except pygame.error:
            self.joystick = None
            return False

    def gatillo_derecho_presionado(self):
        """Detecta RT/R2 en la distribución de ejes más común de SDL."""
        return self._eje(self.EJE_GATILLO_DERECHO) > 0.5

    def accion_menu(self, evento):
        """Convierte cruceta, stick y botones en acciones de interfaz."""
        if evento.type == pygame.JOYBUTTONDOWN:
            if evento.button == self.BOTON_ACEPTAR:
                return "aceptar"
            if evento.button == self.BOTON_CANCELAR:
                return "cancelar"
            if evento.button == self.BOTON_PAUSA:
                return "pausa"

        if evento.type == pygame.JOYHATMOTION:
            x, y = evento.value
            if y > 0:
                return "arriba"
            if y < 0:
                return "abajo"
            if x < 0:
                return "izquierda"
            if x > 0:
                return "derecha"

        if evento.type != pygame.JOYAXISMOTION or evento.axis not in (0, 1):
            return None

        nombre_eje = "x" if evento.axis == 0 else "y"
        if abs(evento.value) < self.ZONA_MUERTA:
            self.eje_menu_activo[nombre_eje] = False
            return None

        if self.eje_menu_activo[nombre_eje] or abs(evento.value) < self.UMBRAL_MENU:
            return None

        self.eje_menu_activo[nombre_eje] = True
        if evento.axis == 0:
            return "derecha" if evento.value > 0 else "izquierda"
        return "abajo" if evento.value > 0 else "arriba"
