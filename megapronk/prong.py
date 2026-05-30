import pygame
import math 
import os
ruta_actual = os.path.dirname(__file__)

class Prongs:
    def __init__(self, mapa):
        self.prongs = [] 
        self.mapa = mapa

    def asignarProng(self, tecla, prong, velocidad = 4):
        self.prongs.append(Especial(tecla, prong, velocidad,  self.mapa))

    def aplicarCambio(self, funcion, especial, magnitud):
        funcion(especial, especial.prong, magnitud)
    
class Especial:
    def __init__(self, tecla, prong, velocidad, mapa):
        self.speed = velocidad
        self.damage = 10
        self.multiDamage = 1
        self.multiArea = 1
        self.proyectiles = []
        self.cooldown_time = 5
        self.cooldown = 0.0
        self.tecla = tecla
        self.Prong = prong(velocidad, self, mapa, self.damage * self.multiDamage, self.multiArea)
        self.mapa = mapa

    def puedeUsar(self):
        return self.cooldown <= 0.0

    def usar(self):
        self.cooldown = self.cooldown_time

    def nuevoProyectil(self, dir, pos):
        if not self.puedeUsar():
            return False
        self.usar()
        self.Prong.lanzarProyectil(dir, pos)
        return True

    def eliminarProyectil(self, proyectil):
        self.proyectiles.remove(proyectil)

    def updateProyectiles(self, enemigos):
        for proyectil in self.proyectiles:
            proyectil.update(enemigos)

    def update(self, dt, enemigos):
        if self.cooldown > 0.0:
            self.cooldown -= dt
            if self.cooldown < 0.0:
                self.cooldown = 0.0
        self.updateProyectiles(enemigos)

class Proyectil:
    def __init__(self, dir, pos, velocidad, danio, esp, tiempo, dimensiones, mapa):
        self.posicion = pos
        self.damage = danio
        self.dimension = dimensiones
        self.dirreccion = dir
        self.speed = velocidad
        self.tiempoVida = tiempo
        self.temporizador = pygame.time.get_ticks()
        self.especial = esp
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
        self.mapa = mapa
        self.enemigosGolpeados = []

    def CalcularPos(self):
        self.posicion[0] += math.cos(self.dirreccion) * self.speed
        self.posicion[1] += math.sin(self.dirreccion) * self.speed

    def update(self, enemigos):
        self.CalcularPos()
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
        
        if self.colisionParedes():
            return

        self.colisionEnemigos(enemigos)

        if pygame.time.get_ticks() - self.temporizador > self.tiempoVida * 1000:
            self.especial.eliminarProyectil(self)

    def colisionParedes(self):
        for pared in self.mapa.paredes:
                if self.rectangulo.colliderect(pared):
                    self.especial.eliminarProyectil(self)
                    return True
        return False
    
    def colisionEnemigos(self, enemigos):
        for enemigo in enemigos:
            if enemigo not in self.enemigosGolpeados:
                enemigo_rect = pygame.Rect(enemigo.x,enemigo.y,enemigo.tamano_x,enemigo.tamano_y)
                if self.rectangulo.colliderect(enemigo_rect):
                    enemigo.vida -= self.damage
                    self.enemigosGolpeados.append(enemigo)
                
                
class ProyectilOscilante(Proyectil):
    def __init__(self, dir, pos, velocidad, danio, esp, tiempo, dimensiones, mapa, r = 1, amplitud=200, frecuencia=0.05):
        super().__init__(dir, list(pos), velocidad, danio, esp, tiempo, dimensiones,mapa)
        
        self.base_pos = list(pos)
        self.amplitud = amplitud    
        self.frecuencia = frecuencia  
        self.distancia_recorrida = 0
        self.sentido = r

    def CalcularPos(self):
        self.distancia_recorrida += self.sentido
        
        self.base_pos[0] += math.cos(self.dirreccion) * self.speed
        self.base_pos[1] += math.sin(self.dirreccion) * self.speed

        perp_x = -math.sin(self.dirreccion)
        perp_y = math.cos(self.dirreccion)

        onda = math.sin(self.distancia_recorrida * self.frecuencia) * self.amplitud

        self.posicion[0] = self.base_pos[0] + perp_x * onda
        self.posicion[1] = self.base_pos[1] + perp_y * onda

class ProyectilBomba(Proyectil):
    def __init__(self, dir, pos, velocidad, danio, esp, tiempo, dimensiones, mapa):
        super().__init__(dir, list(pos), velocidad, danio, esp, tiempo, dimensiones,mapa)
        self.tiempoVida = 1
        self.estado = 0
        self.temporizadorexplosion = 0

    def update(self, enemigos):
        
        if self.estado == 0:
            self.CalcularPos()
            self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
        
            if self.colisionParedes():
                self.CrearExplosion()
                return

            if self.colisionEnemigos(enemigos):
                self.CrearExplosion()
                return

            if pygame.time.get_ticks() - self.temporizador > self.tiempoVida * 1000:
                self.CrearExplosion()
                return
        else:
            
            self.colisionExplosion(enemigos)

            if pygame.time.get_ticks() - self.temporizadorexplosion > 0.2 * 1000:
                self.especial.eliminarProyectil(self)

    def CrearExplosion(self):
        self.dimension = [self.dimension[0] * 5, self.dimension[1] * 5]
        self.estado = 1
        self.temporizadorexplosion = pygame.time.get_ticks()
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
    
    def colisionParedes(self):
        for pared in self.mapa.paredes:
                if self.rectangulo.colliderect(pared):
                    return True
        return False

    def colisionEnemigos(self, enemigos):
        for enemigo in enemigos:
                enemigo_rect = pygame.Rect(enemigo.x,enemigo.y,enemigo.tamano_x,enemigo.tamano_y)
                if self.rectangulo.colliderect(enemigo_rect):
                    return True
        return False
    
    def colisionExplosion(self, enemigos):
        for enemigo in enemigos:
            if enemigo not in self.enemigosGolpeados:
                enemigo_rect = pygame.Rect(enemigo.x,enemigo.y,enemigo.tamano_x,enemigo.tamano_y)
                if self.rectangulo.colliderect(enemigo_rect):
                    enemigo.vida -= self.damage
                    self.enemigosGolpeados.append(enemigo)

class Prong:
    def __init__(self, velocidad, esp, mapa, danio, multiarea):
        self.dimensionOriginal = [80, 80]
        self.dimension = [self.dimensionOriginal[0] * multiarea, self.dimensionOriginal[1] * multiarea]
        self.speed = velocidad
        self.tiempoVida = 5
        self.especial = esp
        self.mapa = mapa
        self.damage = danio
        self.icono = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "disparo_pronk.png"))
        self.icono = pygame.transform.smoothscale(self.icono, (130, 130))
    
    def lanzarProyectil(self, dir, pos):
        proyectil = Proyectil(dir, pos, self.speed * 4, self.damage, self.especial, 5, self.dimension, self.mapa)
        self.especial.proyectiles.append(proyectil)

class BolaFuego(Prong):
    def __init__(self, velocidad, esp, mapa, danio, multiarea):
        super().__init__(velocidad, esp, mapa, danio, multiarea)
        self.dimension = [50 *  multiarea, 50 *  multiarea]
        self.icono = pygame.image.load(
        os.path.join(ruta_actual, "assets", "ui", "bolafuego_pronk.png"))
        self.icono = pygame.transform.smoothscale(self.icono, (135, 135))

    def lanzarProyectil(self, dir, pos):
        proyectil = ProyectilOscilante(dir, pos, self.speed, self.damage, self.especial, 5, self.dimension, self.mapa, 1)
        self.especial.proyectiles.append(proyectil)
        proyectil = ProyectilOscilante(dir, pos, self.speed, self.damage, self.especial, 5, self.dimension, self.mapa, -1)
        self.especial.proyectiles.append(proyectil)

class ProngBomba(Prong):
    def __init__(self, velocidad, esp, mapa, danio, multiarea):
        super().__init__(velocidad, esp, mapa, danio, multiarea)
        self.dimension = [30 * multiarea, 30 * multiarea]


    def lanzarProyectil(self, dir, pos):
        proyectil = ProyectilBomba(dir, pos, self.speed * 4, self.damage, self.especial, 5, self.dimension, self.mapa)
        self.especial.proyectiles.append(proyectil)

class Principal:
    def __init__(self):
        self.costo = 10
        self.radio = 10
        self.damage = 10
        self.multiDamage = 1
        self.speed = 8
        self.proyectiles = []
        self.multiDimensiones = 1
        self.cooldown_time = 0.3  
        self.cooldown = 0.0
        self.set = SetLigero(self.damage * self.multiDamage, self, self.multiDimensiones)
        self.hitbox = [] 

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

    def updateHitbox(self, pos, damage):
        for x in self.hitbox:
            x.update(pos, damage)

    def update(self, dt, pos, damage):
        if self.cooldown > 0.0:
            self.cooldown -= dt
            if self.cooldown < 0.0:
                self.cooldown = 0.0

        self.updateHitbox(pos, damage) 

class SetAtaque:
    def __init__(self, daño, prin, dimensiones):
        self.actAtaque = 0
        self.damage = daño
        self.ultimoAtaque = 0
        self.principal = prin
        self.dimensionesMulti = dimensiones

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
    def __init__(self, daño, prin, dimensiones):
        super().__init__(daño, prin, dimensiones)
        self.intervalo = 1
        self.tiempo = 0.3
        self.damage = daño

    def atacar(self, pos, dir, tamano):
        if pygame.time.get_ticks() - self.ultimoAtaque > self.intervalo * 1000:
            self.actAtaque = 0

        coseno = math.cos(dir)
        seno = math.sin(dir)

        largo = 200 * self.dimensionesMulti
        corto = 120 * self.dimensionesMulti

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
        self.damage = prin.damage
        self.tiempoVida = tiempo
        self.temporizador = pygame.time.get_ticks()
        self.principal = prin
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])
        self.enemigosGolpeados = []

    def update(self, pos, enemigos):
        self.posicion = self.operar(self.expresion, pos)
        self.rectangulo = pygame.Rect(self.posicion[0] - self.dimension[0] / 2, self.posicion[1] - self.dimension[1] / 2, self.dimension[0],self.dimension[1])

        self.colisionEnemigos(enemigos)

        if pygame.time.get_ticks() - self.temporizador > self.tiempoVida * 1000:
            self.principal.eliminarHitbox(self)
    
    def operar(self, func, a):
        return func(a)  
    
    def colisionEnemigos(self, enemigos):
        for enemigo in enemigos:
            if enemigo not in self.enemigosGolpeados:
                enemigo_rect = pygame.Rect(enemigo.x,enemigo.y,enemigo.tamano_x,enemigo.tamano_y)
                if self.rectangulo.colliderect(enemigo_rect):
                    enemigo.vida -= self.damage
                    self.enemigosGolpeados.append(enemigo)
