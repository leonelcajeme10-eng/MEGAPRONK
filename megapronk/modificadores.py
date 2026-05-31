def damageAumento(esp, prong, aumento):
    esp.damage += aumento
    prong.damage += aumento 

def damageAumentoSet(prin, set, aumento):
    prin.damage += aumento
    set.damage += aumento 

def disminuirCooldown(esp, prong, decremento):
    esp.cooldown_time -= decremento

def aumentarVelocidad(jugador, aumento):
    jugador.speed += aumento

def aumentoProbCrit(esp , prong, aumento):
    prong.probCrit += aumento

def aumentoCrit(esp , prong, aumento):
    prong.multiCrit += aumento

def aumentoProbCritSet(prin , set, aumento):
    set.probCrit += aumento

def aumentoCritSet(prin , set, aumento):
    set.multiCrit += aumento