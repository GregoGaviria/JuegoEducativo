import math
import random
import pygame
import globVariables
import config


# sistema de particulas ambientales para el mundo: chispas flotantes,
# polen, motas doradas. se reciclan cuando salen de pantalla.
# no es un motor generico, es solo para polish visual del overworld
# y para spawns puntuales en combate.

class _Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "maxLife", "r", "color")

    def __init__(self, x, y, vx, vy, life, r, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.maxLife = life
        self.r = r
        self.color = color


_ambient = []
_burst = []
_lastSpawn = 0


def init():
    global _ambient, _burst, _lastSpawn
    _ambient = []
    _burst = []
    _lastSpawn = 0


def _newMote():
    x = random.uniform(0, config.WIN_WIDTH)
    y = random.uniform(0, config.WIN_HEIGHT)
    vx = random.uniform(-0.15, 0.15)
    vy = random.uniform(-0.5, -0.15)
    life = random.randint(180, 360)
    r = random.choice((1, 1, 2, 2, 3))
    # dorados y verdes suaves
    color = random.choice((
        (255, 240, 160),
        (220, 255, 180),
        (255, 220, 120),
    ))
    return _Particle(x, y, vx, vy, life, r, color)


# spawn disperso: mantiene ~60 motas flotando todo el tiempo
def updateAmbient():
    global _lastSpawn
    now = pygame.time.get_ticks()
    if len(_ambient) < 60 and now - _lastSpawn > 90:
        _ambient.append(_newMote())
        _lastSpawn = now
    alive = []
    for p in _ambient:
        p.x += p.vx
        p.y += p.vy
        p.life -= 1
        if (p.life > 0 and -10 < p.x < config.WIN_WIDTH + 10
                and -10 < p.y < config.WIN_HEIGHT + 10):
            alive.append(p)
    _ambient[:] = alive


# explosion radial de chispas (ej: al pegarle al enemigo en combate)
def spawnBurst(x, y, count=14, color=(255, 230, 140)):
    for _ in range(count):
        ang = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 4.5)
        _burst.append(_Particle(
            x, y,
            math.cos(ang) * speed,
            math.sin(ang) * speed,
            random.randint(20, 40),
            random.choice((2, 3, 3, 4)),
            color
        ))


def updateBursts():
    alive = []
    for p in _burst:
        p.x += p.vx
        p.y += p.vy
        p.vy += 0.12  # gravedad suave
        p.vx *= 0.96
        p.life -= 1
        if p.life > 0:
            alive.append(p)
    _burst[:] = alive


def _draw(pool):
    surf = globVariables.DISPLAYSURF
    for p in pool:
        t = p.life / p.maxLife
        alpha = int(230 * t)
        if alpha <= 0:
            continue
        # dibujar con pequeño halo (circulo grande translucido + nucleo)
        s = pygame.Surface((p.r * 4, p.r * 4), pygame.SRCALPHA)
        halo = (*p.color, alpha // 3)
        core = (*p.color, alpha)
        pygame.draw.circle(s, halo, (p.r * 2, p.r * 2), p.r * 2)
        pygame.draw.circle(s, core, (p.r * 2, p.r * 2), p.r)
        surf.blit(s, (p.x - p.r * 2, p.y - p.r * 2))


def drawAmbient():
    _draw(_ambient)


def drawBursts():
    _draw(_burst)


