import pygame
from player import Player
import os
import random
ruta_actual = os.path.dirname(__file__)

class Mapa:

    def __init__(self):

        # es la forma del mapa , '#' significa pared y '.' significa camino
        self.mapa = [
"###########################################################################################################",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"#.........................................................................................................#",
"###########################################################################################################",
]
        self.size = 256
        self.paredes = []
        self.calcular_paredes()
        self.suelo_base = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "suelo.png")).convert()
        self.suelo_base = pygame.transform.scale(self.suelo_base, (256, 256))
        self.suelo_final = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "suelo_final.png")).convert()
        self.suelo_final = pygame.transform.scale(self.suelo_final, (256, 256))
        self.suelo_desgaste = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "suelo_desgaste.jpg")).convert()
        self.suelo_desgaste = pygame.transform.scale(self.suelo_desgaste, (256, 256))
        self.ancho_mundo = len(self.mapa[0]) * self.size
        self.alto_mundo = len(self.mapa) * self.size
        self.tiles = []
        self.cuadro1 = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "cuadro1.png")).convert_alpha()
        self.cuadro1 = pygame.transform.smoothscale(self.cuadro1, (250, 250))
        self.cuadro2 = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "cuadro2.png")).convert_alpha()
        self.cuadro2 = pygame.transform.smoothscale(self.cuadro2, (250, 250))
        self.cuadro3 = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "cuadro3.png")).convert_alpha()
        self.cuadro3 = pygame.transform.smoothscale(self.cuadro3, (250, 250))
        self.cuadro4 = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "cuadro4.png")).convert_alpha()
        self.cuadro4 = pygame.transform.smoothscale(self.cuadro4, (250, 250))
        self.cuadro5 = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "cuadro5.png")).convert_alpha()
        self.cuadro5 = pygame.transform.smoothscale(self.cuadro5, (250, 250))
        self.cuadro6 = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "cuadro6.png")).convert_alpha()
        self.cuadro6 = pygame.transform.smoothscale(self.cuadro6, (250, 250))
        self.alfombra = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "alfombra.png")).convert_alpha()
        self.alfombra = pygame.transform.smoothscale(self.alfombra, (400, 400))
        self.libros = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "libros.png")).convert_alpha()
        self.libros = pygame.transform.smoothscale(self.libros, (120, 120))
        self.petalos = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "petalos.png")).convert_alpha()
        self.petalos = pygame.transform.smoothscale(self.petalos, (120, 120))
        self.sangre = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "petalos.png")).convert_alpha()
        self.sangre = pygame.transform.smoothscale(self.sangre, (100, 100))
        self.alfombra2 = pygame.image.load(os.path.join(ruta_actual, "assets", "images", "alfombra2.png")).convert_alpha()
        self.alfombra2 = pygame.transform.smoothscale(self.alfombra2, (500, 400))
        self.imagenes_decoraciones = [
            self.cuadro1,
            self.cuadro2,
            self.cuadro3,
            self.cuadro4,
            self.cuadro5,
            self.cuadro6,
            self.alfombra,
            self.alfombra2,
            self.libros,
            self.petalos,
            self.sangre
        ]

        self.decoraciones = []
        self.generar_decoraciones()

        for fila in range(len(self.mapa)):
            fila_tiles = []
            for columna in range(len(self.mapa[fila])):
                if random.randint(1, 10) > 7:
                    fila_tiles.append("desgaste")
                else:
                    fila_tiles.append("base")
            self.tiles.append(fila_tiles)

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
        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):
                tile = self.mapa[fila][columna]
                x = columna * self.size
                y = fila * self.size
                
                if tile == "#":
                    pantalla.blit(self.suelo_final, (x - camara.x, y - camara.y))
                else:
                    tipo = self.tiles[fila][columna]
                    pantalla.blit(self.suelo_base, (x - camara.x, y - camara.y))
                    
            for decoracion in self.decoraciones:
                pantalla.blit(
                decoracion["imagen"],
                        (
                            decoracion["x"] - camara.x,
                            decoracion["y"] - camara.y
                        )
                    )

    def update(self,pantalla,camara):
        self.dibujar_mapa(pantalla,camara)
        
    def generar_decoraciones(self):
        for fila in range(len(self.mapa)):
            for columna in range(len(self.mapa[fila])):

                tile = self.mapa[fila][columna]

                if tile == ".":
                    # Probabilidad de que aparezca decoracion en ese tile
                    if random.randint(1, 100) <= 4:

                        imagen = random.choice(self.imagenes_decoraciones)

                        x_tile = columna * self.size
                        y_tile = fila * self.size

                        rect = imagen.get_rect()

                        # Centrar decoracion en el tile
                        x = x_tile + self.size // 2 - rect.width // 2
                        y = y_tile + self.size // 2 - rect.height // 2

                        self.decoraciones.append({
                            "imagen": imagen,
                            "x": x,
                            "y": y
                        })     



        
