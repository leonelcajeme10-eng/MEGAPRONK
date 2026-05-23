import pygame
import math 

class Especial:
    def __init__(self):
        self.costo = 10
        self.radio = 10
        self.speed = 8
        self.proyectiles = []
        self.cooldown_time = 0.5  # segundos entre usos
        self.cooldown = 0.0

    def puede_usar(self):
        return self.cooldown <= 0.0

    def usar(self):
        self.cooldown = self.cooldown_time

    def nuevoProyectil(self, dir, pos):
        if not self.puede_usar():
            return False

        self.usar()
        proyectil = Proyectil(self.radio, dir, pos, self)
        self.proyectiles.append(proyectil)
        return True

    def eliminarProyectil(self, proyectil):
        self.proyectiles.remove(proyectil)

    def updateProyectiles(self):
        for proyectil in self.proyectiles:
            proyectil.update()

    def update(self, dt):
        if self.cooldown > 0.0:
            self.cooldown -= dt
            if self.cooldown < 0.0:
                self.cooldown = 0.0
        self.updateProyectiles()

class Proyectil:
    def __init__(self, rad, dir, pos, esp):
        self.posicion = pos
        self.costo = 10
        self.radio = rad
        self.dirreccion = dir
        self.speed = 4
        # apuntador a clase especial
        self.especial = esp

    def update(self):
        self.posicion[0] += math.cos(self.dirreccion) * self.speed
        self.posicion[1] += math.sin(self.dirreccion) * self.speed
        if self.posicion[0] < 0 or self.posicion[0] > 1920 or self.posicion[1] < 0 or self.posicion[1] > 1080:
            self.especial.eliminarProyectil(self)