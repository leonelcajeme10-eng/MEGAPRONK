import pygame
import math 

class Especial:
    def __init__(self):
        self.costo = 10
        self.speed = 8
        self.damage = 10
        self.proyectiles = []
        self.cooldown_time = 0.1
        self.cooldown = 0.0

    def puedeUsar(self):
        return self.cooldown <= 0.0

    def usar(self):
        self.cooldown = self.cooldown_time

    def nuevoProyectil(self, dir, pos):
        if not self.puedeUsar():
            return False

        self.usar()
        proyectil = Proyectil(dir, pos, self, 2)
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

    def atacar(self, pos, dir, tamano):
        if self.puedeUsar():
            self.set.atacar(pos, dir, tamano)
            self.usar()

    def puedeUsar(self):
        return self.cooldown <= 0.0

    def usar(self):
        self.cooldown = self.cooldown_time

    def nuevaHitbox(self, htbx):
        self.hitbox.append(htbx)

    def eliminarHitbox(self, htbx):
        self.hitbox.remove(htbx)

    def updateHitbox(self, pos):
        for x in self.hitbox:
            x.update(pos)

    def update(self, dt, pos):
        if self.cooldown > 0.0:
            self.cooldown -= dt
            if self.cooldown < 0.0:
                self.cooldown = 0.0

        self.updateHitbox(pos) 

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
        
    def atacar(self, pos, dir, tamano):
        if pygame.time.get_ticks() - self.ultimoAtaque > self.intervalo * 1000:
            self.actAtaque = 0
        coseno = math.cos(dir)
        seno = math.sin(dir)

        fwd_x, fwd_y = coseno, seno
        perp_x, perp_y = -seno, coseno
        perp_len = math.hypot(perp_x, perp_y)
        if perp_len != 0:
            perp_x /= perp_len
            perp_y /= perp_len

        largo = 80
        corto = 40

        if abs(coseno) > abs(seno):
            dimensiones = [corto, largo]
        else:
            dimensiones = [largo, corto]

        base_dist = max(tamano[0], tamano[1]) / 2 + 20

        def mk_hitbox(shift_perp, dims=None, tiempo=0.2, forward_offset=0):
            d = dims if dims is not None else dimensiones
            expr = (lambda posicion, fx=fwd_x, fy=fwd_y, px=perp_x, py=perp_y, bd=base_dist, sp=shift_perp, fo=forward_offset:
                    [posicion[0] + fx * (bd + fo) + px * sp, posicion[1] + fy * (bd + fo) + py * sp])
            return Hitbox(expr, pos, d, tiempo, self.principal)

        match self.actAtaque:
            case 0:
                # desplazado 30px a la izquierda (desde el punto de vista del ataque)
                hitbox = mk_hitbox(-30)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1
            case 1:
                hitbox = mk_hitbox(30)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1
            case 2:
                # otra vez a la izquierda
                hitbox = mk_hitbox(-30)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1
            case 3:
                # desplazado a la derecha
                hitbox = mk_hitbox(30)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1
            case 4:
                # final con mayor dimensión perpendicular
                if abs(coseno) > abs(seno):
                    final_dims = [corto + 80, largo + 30]
                else:
                    final_dims = [largo + 30, corto + 80]
                hitbox = mk_hitbox(0, final_dims, 0.2, 40)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque = 0
            case _:
                self.actAtaque = 0

        self.ultimoAtaque = pygame.time.get_ticks()

class Hitbox():
    def __init__(self, exp, pos, dim, tiempo, prin):
        self.expresion = exp
        self.posicion = self.operar(self.expresion, pos)
        self.dimension = dim
        self.tiempoVida = tiempo
        self.temporizador = pygame.time.get_ticks()
        self.principal = prin

    def update(self, pos):
        # si ha pasado el tiempo de vida, eliminar la hitbox
        self.posicion = self.operar(self.expresion, pos)

        if pygame.time.get_ticks() - self.temporizador > self.tiempoVida * 1000:
            self.principal.eliminarHitbox(self)
    
    def operar(self, func, a):
        return func(a)
        

class Proyectil:
    def __init__(self, dir, pos, esp, tiempo):
        self.posicion = pos
        self.costo = 10
        self.dimension = [10, 10]
        self.dirreccion = dir
        self.speed = 20
        self.tiempoVida = tiempo
        self.temporizador = pygame.time.get_ticks()
        # apuntador a clase especial
        self.especial = esp

    def update(self):
        self.posicion[0] += math.cos(self.dirreccion) * self.speed
        self.posicion[1] += math.sin(self.dirreccion) * self.speed
        if pygame.time.get_ticks() - self.temporizador > self.tiempoVida * 1000:
            self.especial.eliminarProyectil(self)