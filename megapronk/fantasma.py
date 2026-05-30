from enemy import Enemy

class Fantasma(Enemy):
    COLOR = "white"
    SPEED = 100
    VIDA = 100
    DAMAGE = 10
    TAMANO_X = 50
    TAMANO_Y = 50
    EXP = 30
    def __init__(self, camara):
        super().__init__(camara)