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

    def mk_hitbox(self, dir, tamano, dims, shift_perp = 0, forward_offset=0):
            coseno = math.cos(dir)
            seno = math.sin(dir)

            d = dims
            if abs(coseno) > abs(seno):
                ancho, largo = dims
            else:
                largo, ancho = dims

            b_dist = max(tamano[0], tamano[1]) / 2 + ancho / 2

            fwd_x, fwd_y = coseno, seno
            perp_x, perp_y = -seno, coseno
            perp_len = math.hypot(perp_x, perp_y)
            
            if perp_len != 0:
                perp_x /= perp_len
                perp_y /= perp_len

            expr = (lambda posicion, fx=fwd_x, fy=fwd_y, px=perp_x, py=perp_y, bd= b_dist, sp=shift_perp, fo=forward_offset:
                    [posicion[0] + fx * (bd + fo) + px * sp, posicion[1] + fy * (bd + fo) + py * sp])
            return expr
    
class SetLigero(SetAtaque):
    def __init__(self, daño, prin):
        super().__init__(daño, prin)
        self.intervalo = 0.4
        self.tiempo = 0.2
        self.damage = daño

    def atacar(self, pos, dir, tamano):
        if pygame.time.get_ticks() - self.ultimoAtaque > self.intervalo * 1000:
            self.actAtaque = 0

        coseno = math.cos(dir)
        seno = math.sin(dir)

        largo = 200
        corto = 120

        if abs(coseno) > abs(seno):
            dimensiones = (corto, largo)
        else:
            dimensiones = (largo, corto)

        match self.actAtaque:
            case 0:
                expr = self.mk_hitbox(dir, tamano, dimensiones, largo / 4)  
                hitbox = Hitbox(expr, pos, dimensiones, self.tiempo, self.principal)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1

            case 1:
                expr = self.mk_hitbox(dir, tamano, dimensiones, - largo / 4)
                hitbox = Hitbox(expr, pos, dimensiones, self.tiempo, self.principal)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1

            case 2:
                expr = self.mk_hitbox(dir, tamano, dimensiones, largo / 4)
                hitbox = Hitbox(expr, pos, dimensiones, self.tiempo, self.principal)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1

            case 3:
                expr = self.mk_hitbox(dir, tamano, dimensiones, - largo / 4)
                hitbox = Hitbox(expr, pos, dimensiones, self.tiempo, self.principal)
                self.principal.nuevaHitbox(hitbox)
                self.actAtaque += 1

            case 4:
                if abs(coseno) > abs(seno):
                    final_dims = [corto + corto, largo + largo / 4]
                else:
                    final_dims = [largo + largo / 4, corto + corto]

                expr = self.mk_hitbox(dir, tamano, final_dims)
                hitbox = Hitbox(expr, pos, final_dims, self.tiempo, self.principal)

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
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
    
    def update(self, pos):
        self.posicion = self.operar(self.expresion, pos)
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
    
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
        self.speed = 4
        self.tiempoVida = tiempo
        self.temporizador = pygame.time.get_ticks()
        # apuntador a clase especial
        self.especial = esp
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
    

    def CalcularPos(self):
        self.posicion[0] += math.cos(self.dirreccion) * self.speed
        self.posicion[1] += math.sin(self.dirreccion) * self.speed

    def update(self):
        self.CalcularPos()
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
        if pygame.time.get_ticks() - self.temporizador > self.tiempoVida * 1000:
            self.especial.eliminarProyectil(self)

class ProyectilOscilante(Proyectil):
    def __init__(self, dir, pos, esp, tiempo, amplitud=30, frecuencia=0.03):
        super().__init__(dir, pos, esp, tiempo)
        self.base_pos = pos
        self.amplitud = amplitud    
        self.frecuencia = frecuencia  
        self.distancia_recorrida = 0  

    def CalcularPos(self):
        self.base_pos[0] += math.cos(self.dirreccion) * self.speed
        self.base_pos[1] += math.sin(self.dirreccion) * self.speed

        perp_x = -math.sin(self.dirreccion)
        perp_y = math.cos(self.dirreccion)

        angulo_onda = (self.distancia_recorrida - self.speed) * self.frecuencia
        onda = math.sin(angulo_onda) * self.amplitud

        self.posicion[0] = self.base_pos[0] + perp_x * onda
        self.posicion[1] = self.base_pos[1] + perp_y * onda