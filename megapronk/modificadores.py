def danioBaseAumento(esp, prong, aumento):
    esp.damage += aumento
    prong.damage += esp.damage * esp.multiDamage

def danioMulti(esp, prong, multi):
    esp.multiDamage *= multi
    prong.damage += esp.damage * esp.multiDamage

def prongAumentoArea(esp, prong, aumento):
    esp.multiArea += aumento
    prong.dimensiones = [prong.dimensionOriginal[0] * esp.multiArea, prong.dimensionOriginal[1] * esp.multiarea]

def prongMultiArea(esp, prong, multi):
    esp.multiArea *= multi
    prong.dimensiones = [prong.dimensionOriginal[0] * esp.multiArea, prong.dimensionOriginal[1] * esp.multiarea]

def disminuirCooldown(esp, prong, decremento):
    esp.cooldown_time -= decremento

def prongAumentoArea(esp, set, aumento):
    esp.multiArea += aumento

def prongAumentoArea(esp, set, multi):
    esp.multiArea *= multi
