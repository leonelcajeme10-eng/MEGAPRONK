import pygame
from player import Player
import math
import random
from camara import Camara
import Enemy



class Mariposa(Enemy):
    COLOR = "red"
    SPEED = 120
    VIDA = 100
    DAMAGE = 10
    TAMANO_X = 50
    TAMANO_Y = 50

    def __init__(self,camara):
        super().__init__()
        self.tamano_x = self.TAMANO_X
        self.tamano_y = self.TAMANO_Y
        self.vida = self.VIDA
        self.speed = self.SPEED
        self.damage = self.DAMAGE


        
