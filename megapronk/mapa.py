import pygame
from player import Player

class Mapa:

    def __init__(self):

        # es la forma del mapa , '#' significa pared y '.' significa camino
        self.mapa = [
    "##########################",
    "#........................#",
    "#........................#",
    "#........................#",
    "#....####....####........#",
    "#........................#",
    "#........................#",
    "#........................#",
    "###########....###########"
    ]
        self.size = 32
        self.paredes = []
        self.calcular_paredes()

    def calcular_paredes(self):
        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):
                tile = self.mapa[fila][columna]
                
                if tile == '#':
                    x = columna * self.size
                    y = fila * self.size 
                    pared_rect = pygame.Rect(x,y,self.size,self.size)
                    self.paredes.append(pared_rect)
                    
                    


    def dibujar_mapa(self,pantalla,camara):
        
        for paredes in self.paredes:
            pygame.draw.rect(pantalla,"blue",camara.aplicar_rect(paredes))


            

    def update(self,pantalla,camara):
        self.dibujar_mapa(pantalla,camara)
        
        



        
