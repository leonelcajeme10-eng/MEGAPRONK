def damageAumento(esp, prong, aumento):
    esp.damage += aumento
    prong.damage += esp.damage * esp.multiDamage

def disminuirCooldown(esp, prong, decremento):
    esp.cooldown_time -= decremento