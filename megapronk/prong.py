import pygame
import math 

class Especial:
    def __init__(self):
        self.costo = 10
        self.speed = 8
        self.damage = 10
        self.proyectiles = []
        self.cooldown_time = 0.5
        self.cooldown = 0.0

    def puedeUsar(self):
        return self.cooldown <= 0.0

    def usar(self):
        self.cooldown = self.cooldown_time

    def nuevoProyectil(self, dir, pos):
        if not self.puedeUsar():
            return False

        self.usar()
        proyectil = Proyectil(dir, pos, self)
        self.proyectiles.append(proyectil)
        return True

    def eliminarProyectil(self, proyectil):
        self.proyectiles.remove(proyectil)

    def updateProyectiles(self):
        for proyectil in self.proyectiles:
            proyectil.update()

    def update(self, dt):
        if self.cooldown > 0.0:
            self.cooldown -= dt
            if self.cooldown < 0.0:
                self.cooldown = 0.0
        self.updateProyectiles()

class Principal:
    def __init__(self):
        self.costo = 10
        self.radio = 10
        self.damage = 10
        self.speed = 8
        self.proyectiles = []
        self.cooldown_time = 0.2  # segundos entre usos
        self.cooldown = 0.0
        self.set = SetLigero(self.damage, self)
        self.hitbox = [] # se almacena el rectangulo de la hitbox del ataque

    def atacar(self, pos):
        if self.puedeUsar():
            self.set.atacar(pos)
            self.usar()

    def puedeUsar(self):
        return self.cooldown <= 0.0

    def usar(self):
        self.cooldown = self.cooldown_time

    def nuevaHitbox(self, htbx):
        self.hitbox.append(htbx)

    def eliminarHitbox(self, htbx):
        self.hitbox.remove(htbx)

    def updateHitbox(self, dpos):
        for x in self.hitbox:
            x.update(dpos)

    def update(self, dt, dpos):
        if self.cooldown > 0.0:
            self.cooldown -= dt
            if self.cooldown < 0.0:
                self.cooldown = 0.0

        self.updateHitbox(dpos) 

class SetAtaque:
    def __init__(self, daño, prin):
        self.actAtaque = 0
        self.damage = daño
        self.ultimoAtaque = 0
        self.principal = prin

class SetLigero(SetAtaque):
    def __init__(self, daño, prin):
        super().__init__(daño, prin)
        self.intervalo = 0.4
        
    def atacar(self, pos, dir = 0.5 * math.pi):
        # reset combo if enough time passed
        if pygame.time.get_ticks() - self.ultimoAtaque > self.intervalo * 1000:
            self.actAtaque = 0

        match self.actAtaque:
            case 1:
                posicion = [pos[0] + math.cos(dir) * 20 - 30, pos[1] + math.sin(dir) * 20 + 20]
                hitbox = Hitbox(posicion, [80, 40], 0.2, self.principal)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1
            case 2:
                posicion = [pos[0] + math.cos(dir) * 20, pos[1] + math.sin(dir) * 20 + 20]
                hitbox = Hitbox(posicion, [110, 80], 0.2, self.principal)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque = 0
            case 0:
                posicion = [pos[0] + math.cos(dir) * 20 + 30, pos[1] + math.sin(dir) * 20 + 20]
                hitbox = Hitbox(posicion, [80, 40], 0.2, self.principal)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1

        self.ultimoAtaque = pygame.time.get_ticks()

class Hitbox():
    def __init__(self, pos, dim, tiempo, prin):
        self.posicion = pos
        self.dimension = dim
        self.tiempoVida = tiempo
        self.temporizador = pygame.time.get_ticks()
        self.principal = prin

    def update(self, dpos):
        # si ha pasado el tiempo de vida, eliminar la hitbox
        self.posicion[0] += dpos[0]
        self.posicion[1] += dpos[1]
        if pygame.time.get_ticks() - self.temporizador > self.tiempoVida * 1000:
            self.principal.eliminarHitbox(self)
        

class Proyectil:
    def __init__(self, dir, pos, esp):
        self.posicion = pos
        self.costo = 10
        self.dimension = [10, 10]
        self.dirreccion = dir
        self.speed = 4
        # apuntador a clase especial
        self.especial = esp

    def update(self):
        self.posicion[0] += math.cos(self.dirreccion) * self.speed
        self.posicion[1] += math.sin(self.dirreccion) * self.speed
        if self.posicion[0] < 0 or self.posicion[0] > 1920 or self.posicion[1] < 0 or self.posicion[1] > 1080:
            self.especial.eliminarProyectil(self)