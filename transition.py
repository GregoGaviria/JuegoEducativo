import math
import random
import pygame
import globVariables


# transicion estilo pokemon: aspas de espiral que crecen desde el centro
# hasta cubrir la pantalla, se dispara el callback de cambio de estado
# en el punto medio, y luego las aspas se recogen revelando la nueva escena.

_active = False
_startTime = 0
_duration = 0
_callback = None
_calledBack = False
_mode = "spiral"
_shakeOffset = (0, 0)

_ARMS = 6
_TURNS = 1.25


def start(callback=None, duration=2500):
    global _active, _startTime, _duration, _callback, _calledBack, _mode
    _active = True
    _startTime = pygame.time.get_ticks()
    _duration = duration
    _callback = callback
    _calledBack = False
    _mode = "spiral"


# intro agresiva para el jefe: pantalla tiembla, flashes rojos, grietas
# que crecen desde el centro y colapsan hacia adentro
def startBoss(callback=None, duration=3200):
    global _active, _startTime, _duration, _callback, _calledBack, _mode
    _active = True
    _startTime = pygame.time.get_ticks()
    _duration = duration
    _callback = callback
    _calledBack = False
    _mode = "boss"


def isActive():
    return _active


# offset de shake aplicado por el mundo/menus durante la transicion del jefe
def getShakeOffset():
    return _shakeOffset


def _drawSpiral(surf, progress, spin):
    # progress: 0 = pantalla limpia, 1 = pantalla totalmente tapada
    w, h = surf.get_size()
    cx, cy = w / 2, h / 2
    radius = math.hypot(w, h)
    armStep = 2 * math.pi / _ARMS
    armWidth = armStep * progress
    rotation = spin * _TURNS * 2 * math.pi
    steps = 10
    for i in range(_ARMS):
        base = i * armStep + rotation
        points = [(cx, cy)]
        for s in range(steps + 1):
            a = base + armWidth * (s / steps)
            points.append((cx + math.cos(a) * radius, cy + math.sin(a) * radius))
        pygame.draw.polygon(surf, (0, 0, 0), points)


# dibuja la intro del jefe: grietas rojas que explotan desde el centro,
# flashes y estatica. agresiva, fuerte. en la segunda mitad el negro se
# abre revelando al jefe
def _drawBossIntro(surf, progress, elapsed):
    w, h = surf.get_size()
    cx, cy = w / 2, h / 2
    radius = math.hypot(w, h)

    # capa de oscuridad que cubre al crecer progress
    if progress >= 1.0:
        surf.fill((0, 0, 0))
    else:
        # grietas / esquirlas rojas agresivas (12 aspas filosas)
        shards = 12
        armStep = 2 * math.pi / shards
        armWidth = armStep * progress * 0.95
        # las aspas alternan color (negro/rojo oscuro) para sensacion jagged
        for i in range(shards):
            base = i * armStep
            color = (90, 10, 15) if (i % 2 == 0) else (0, 0, 0)
            points = [(cx, cy)]
            steps = 8
            for s in range(steps + 1):
                a = base + armWidth * (s / steps)
                # jitter radial en las puntas para que se vean rotas
                jitter = 1.0 if s == 0 or s == steps else (
                    0.88 + 0.12 * math.sin(elapsed * 0.05 + i + s)
                )
                points.append((
                    cx + math.cos(a) * radius * jitter,
                    cy + math.sin(a) * radius * jitter,
                ))
            pygame.draw.polygon(surf, color, points)

    # flash rojo pulsante (mas fuerte en la primera mitad)
    pulse = (math.sin(elapsed * 0.025) + 1) / 2
    flashAlpha = int(160 * pulse * (1 - abs(progress - 1) * 0.6))
    if flashAlpha > 0:
        flash = pygame.Surface((w, h), pygame.SRCALPHA)
        flash.fill((200, 30, 30, flashAlpha))
        surf.blit(flash, (0, 0))


def update():
    global _active, _calledBack, _shakeOffset
    if not _active:
        _shakeOffset = (0, 0)
        return
    now = pygame.time.get_ticks()
    elapsed = now - _startTime
    half = _duration / 2

    if elapsed >= _duration:
        if not _calledBack and _callback is not None:
            _callback()
            _calledBack = True
        _active = False
        _shakeOffset = (0, 0)
        return

    if elapsed < half:
        progress = elapsed / half
    else:
        if not _calledBack and _callback is not None:
            _callback()
            _calledBack = True
        progress = 1 - (elapsed - half) / half

    if _mode == "boss":
        # shake mas fuerte al inicio, se desvanece al final
        intensity = int(20 * (1 - abs(progress - 1) * 0.5))
        _shakeOffset = (
            random.randint(-intensity, intensity),
            random.randint(-intensity, intensity),
        )
        _drawBossIntro(globVariables.DISPLAYSURF, progress, elapsed)
    else:
        _shakeOffset = (0, 0)
        spin = elapsed / _duration
        _drawSpiral(globVariables.DISPLAYSURF, progress, spin)
