from enemy import Enemy

class Mariposa(Enemy):
    COLOR = "pink"
    SPEED = 120
    VIDA = 60
    DAMAGE = 10
    TAMANO_X = 50
    TAMANO_Y = 50
    EXP = 20

    def __init__(self, camara):
        super().__init__(camara)


   
    ANIMACION_MOVIMIENTO = {
        "ruta": "assets/images/bfly_spritesheet.png",
        "columnas": 4,
        "filas": 4,
        "escala": 1,
        "velocidad": 0.12,
        "orden_filas": ["up", "down", "left", "right"]
    }
