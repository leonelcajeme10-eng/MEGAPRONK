def danioBaseAumento(esp, prong, aumento):
    esp.damage += aumento
    prong.damage = esp.damage * esp.multiDamage

def danioMulti(esp, prong, multi):
    esp.multiDamage *= multi
    prong.damage = esp.damage * esp.multiDamage

def prongAumentoArea(esp, prong, aumento):
    esp.multiArea += aumento
    prong.dimension = [prong.dimensionOriginal[0] * esp.multiArea, prong.dimensionOriginal[1] * esp.multiArea]

def prongMultiArea(esp, prong, multi):
    esp.multiArea *= multi
    prong.dimension = [prong.dimensionOriginal[0] * esp.multiArea, prong.dimensionOriginal[1] * esp.multiArea]

def disminuirCooldown(esp, prong, decremento):
    esp.cooldown_time -= decremento

def principalAumentoArea(principal, set, aumento):
    principal.multiDimensiones += aumento
    set.dimensionesMulti = principal.multiDimensiones

def principalMultiArea(principal, set, multi):
    principal.multiDimensiones *= multi
    set.dimensionesMulti = principal.multiDimensiones
