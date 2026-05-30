from enemy import Enemy

class Mariposa(Enemy):
    COLOR = "pink"
    SPEED = 120
    VIDA = 60
    DAMAGE = 10
    TAMANO_X = 50
    TAMANO_Y = 50

    def __init__(self, camara):
        super().__init__(camara)


    
    