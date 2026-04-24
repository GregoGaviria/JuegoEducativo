import menuEntries
import random
import movelist
import combat
import pygame
import config
import globVariables
import gamestate
import audio
import transition
import unittest


class WorldObject():
    def __init__(self, x, y, spritePath, interactFunc, size=None):
        if size is None:
            size = config.SPRITE_SIZE
        # size puede ser int (cuadrado) o tupla (w, h)
        if isinstance(size, tuple):
            w, h = size
        else:
            w, h = size, size
        self.sprite = pygame.transform.scale(
            pygame.image.load(spritePath),
            (w, h)
        )
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.drawSize = (w, h)
        self.interactFunc = interactFunc
        self.solid = False
        # sin animacion por defecto
        self.frames = None
        self.frameIdx = 0
        self.lastFrameTick = 0

    def setAnimation(self, sheetPath, size=None, frameWidth=None):
        if size is None:
            size = self.drawSize
        if isinstance(size, tuple):
            w, h = size
        else:
            w, h = size, size
        sheet = pygame.image.load(sheetPath).convert_alpha()
        frameHeight = sheet.get_height()
        # si no se pasa frameWidth, se asume cuadrado (ancho = alto).
        # los sprites del pack con frames en retrato (ej: arboles)
        # necesitan que se especifique explicitamente.
        if frameWidth is None:
            frameWidth = frameHeight
        count = sheet.get_width() // frameWidth
        self.frames = []
        for i in range(count):
            sub = pygame.Surface(
                (frameWidth, frameHeight), pygame.SRCALPHA
            )
            sub.blit(sheet, (0, 0),
                     (i*frameWidth, 0, frameWidth, frameHeight))
            self.frames.append(pygame.transform.scale(sub, (w, h)))

    def draw(self):
        if self.frames:
            now = pygame.time.get_ticks()
            if now - self.lastFrameTick > 1000 // config.ANIM_FPS:
                self.frameIdx = (self.frameIdx + 1) % len(self.frames)
                self.lastFrameTick = now
            globVariables.DISPLAYSURF.blit(
                self.frames[self.frameIdx], self.rect
            )
        else:
            globVariables.DISPLAYSURF.blit(self.sprite, self.rect)

    def playerwithinrange(self):
        xrange = False
        yrange = False
        if (
            self.rect.centerx-config.INTERACT_RANGE <=
            gamestate.player.worldObject.rect.centerx <=
            self.rect.centerx+config.INTERACT_RANGE
        ):
            xrange = True
        if (
            self.rect.centery-config.INTERACT_RANGE <=
            gamestate.player.worldObject.rect.centery <=
            self.rect.centery+config.INTERACT_RANGE
        ):
            yrange = True
        if xrange and yrange:
            self.interactFunc()


class Player():
    def __init__(self):
        self.worldObject = WorldObject(
            0,
            0,
            "assets/player.png",
            lambda: None
        )
        self.worldObject.setAnimation("assets/player_sheet.png")

        self.combat = combat.CombatUnit(
            name="el jugador",
            baseHP=500,
            baseAttack=100,
            baseDefense=100,
            baseSpatk=100,
            baseSpdef=100,
            baseSpeed=100,
            move0=movelist.getUnitTest(),
            move1=movelist.getIntegrationTest(),
            move2=movelist.getSystemTest(),
            weaknesses=["irritating"],
            resists=["evasive"],
            immunities=[],
            types=["system"]
        )

    def draw(self):
        self.worldObject.draw()


class Wall():
    # variante elegida al azar para que el muro no se vea robotico
    def __init__(self, x, y, variant=None):
        if variant is None:
            variant = random.randint(1, 4)
        self.worldObject = WorldObject(
            x, y,
            f"assets/rock{variant}.png",
            lambda: None,
            size=config.WALL_SIZE
        )
        self.worldObject.solid = True

    def draw(self):
        self.worldObject.draw()

    def playerwithinrange(self):
        # las paredes no son interactuables
        pass


# decoracion puramente visual: no bloquea ni se interactua
class Decoration():
    def __init__(self, x, y, spritePath, size=None, sheet=None,
                 frameWidth=None):
        if size is None:
            size = config.DECO_SIZE
        self.worldObject = WorldObject(
            x, y, spritePath, lambda: None, size=size
        )
        if sheet is not None:
            self.worldObject.setAnimation(sheet, frameWidth=frameWidth)

    def draw(self):
        self.worldObject.draw()

    def playerwithinrange(self):
        pass


def getTree(x, y):
    variant = random.randint(1, 2)
    # los arboles son 192x256 por frame (aspecto retrato): se preserva
    # la proporcion al escalarlos
    return Decoration(
        x, y,
        f"assets/tree{variant}.png",
        size=(120, 160),
        sheet=f"assets/tree{variant}_sheet.png",
        frameWidth=192
    )


def getBush(x, y):
    variant = random.randint(1, 2)
    return Decoration(
        x, y,
        f"assets/bush{variant}.png",
        size=config.DECO_SIZE,
        sheet=f"assets/bush{variant}_sheet.png"
    )


def getSheep(x, y):
    # ovejitas animadas (no interactuables, no solidas)
    return Decoration(
        x, y,
        "assets/sheep.png",
        size=80,
        sheet="assets/sheep_sheet.png"
    )


def getHouse(x, y, variant=None):
    # casitas estaticas, 2:3 de aspecto para no deformarlas
    if variant is None:
        variant = random.randint(1, 3)
    return Decoration(
        x, y,
        f"assets/house{variant}.png",
        size=(128, 192)
    )


# portal (muelle con cartel) que lleva a otra isla al interactuar
class Portal():
    def __init__(self, x, y, targetIsland, targetSpawn, direction="right"):
        def onInteract():
            def switch():
                gamestate.loadIsland(targetIsland, spawn=targetSpawn)
            # transicion corta (espiral) para cambio de isla
            transition.start(switch, duration=1500)
        sprite = (
            "assets/dock-right.png" if direction == "right"
            else "assets/dock-left.png"
        )
        self.worldObject = WorldObject(
            x, y, sprite, onInteract, size=96
        )

    def draw(self):
        self.worldObject.draw()

    def playerwithinrange(self):
        self.worldObject.playerwithinrange()


class Enemy():
    def __init__(self, sprite, combatUnit, x, y, dialog,
                 sheet=None, isBoss=False, size=None):
        self.isBoss = isBoss

        def iniciateBattle():
            # el boss usa final_battle.mp3, el resto main_battle.mp3
            if self.isBoss:
                audio.playBgm(audio.FINAL_BATTLE)
            else:
                audio.startBattleBgm()

            def enter():
                menuEntries.loadBattleMenu(self)
                gamestate.gameloop = "menu"
            # intro agresiva si es el jefe, espiral suave para el resto
            if self.isBoss:
                transition.startBoss(enter, duration=3200)
            else:
                transition.start(enter, duration=2500)
        self.sprite = sprite
        self.worldObject = WorldObject(
            x,
            y,
            sprite,
            iniciateBattle,
            size=size
        )
        if sheet is not None:
            self.worldObject.setAnimation(sheet)

        self.combat = combatUnit
        self.dialog = dialog

    def getRandomDialog(self):
        random.choice(self.dialog)

    def getCombatSprite(self):
        return pygame.transform.scale(
            pygame.image.load(self.sprite),
            (400, 400)
        )

    def draw(self):
        self.worldObject.draw()

    def playerwithinrange(self):
        self.worldObject.playerwithinrange()


def getLibro():
    def libroInteractFunc():
        menuEntries.loadBookMenu()
        gamestate.gameloop = "menu"
    return WorldObject(
        150,
        150,
        "assets/book-icon.png",
        libroInteractFunc,
        size=96
    )


def getEnemyAt(enemy, x, y):
    e = getEnemy(enemy)
    e.worldObject.rect.x = x
    e.worldObject.rect.y = y
    return e


def getBoss(x, y):
    # jefe final: stats altas, se dibuja imponente en el mundo
    bossSize = 300
    return Enemy(
        sprite="assets/boss.png",
        sheet="assets/boss_sheet.png",
        isBoss=True,
        size=bossSize,
        combatUnit=combat.CombatUnit(
            name="Vibecoded Slop",
            baseHP=900,
            baseAttack=140,
            baseDefense=120,
            baseSpatk=110,
            baseSpdef=110,
            baseSpeed=80,
            move0=movelist.getCrash(),
            move1=movelist.getBluescreen(),
            move2=movelist.getRomperInterfazVisual(),
            weaknesses=["system", "integration"],
            resists=["unit"],
            immunities=[],
            types=["boss", "irritating"]
        ),
        x=x,
        y=y,
        dialog=[
            "Vibecoded Slop ruge con furia",
            "Vibecoded Slop te mira con desprecio"
        ]
    )


def getEnemy(enemy):
    match enemy:
        case "crasheador":
            return Enemy(
                sprite="assets/enemy-warrior.png",
                sheet="assets/enemy-warrior_sheet.png",
                combatUnit=combat.CombatUnit(
                    name="crasheador",
                    baseHP=500,
                    baseAttack=115,
                    baseDefense=70,
                    baseSpatk=110,
                    baseSpdef=65,
                    baseSpeed=65,
                    move0=movelist.getCrash(),
                    move1=movelist.getBluescreen(),
                    move2=movelist.getIrritar(),
                    weaknesses=["system"],
                    resists=["unit"],
                    immunities=[],
                    types=["irritating"]
                ),
                x=200,
                y=400,
                dialog=[
                    "el crasheador te muestra una pantalla azul",
                    "el crasheador se tropieza"
                ]
            )
        case "conexion":
            return Enemy(
                sprite="assets/enemy-archer.png",
                sheet="assets/enemy-archer_sheet.png",
                combatUnit=combat.CombatUnit(
                    name="Gwifi",
                    baseHP=500,
                    baseAttack=85,
                    baseDefense=140,
                    baseSpatk=75,
                    baseSpdef=110,
                    baseSpeed=65,
                    move0=movelist.getOutage(),
                    move1=movelist.getIntermitencia(),
                    move2=movelist.getVelocidadBaja(),
                    weaknesses=["integration"],
                    resists=[],
                    immunities=["unit"],
                    types=["network"]
                ),
                x=800,
                y=400,
                dialog=[
                    "el enemigo empieza a hablar muy lento",
                    "el enemigo se cae"
                ]
            )
        case "pulgita":
            return Enemy(
                sprite="assets/enemy-pawn.png",
                sheet="assets/enemy-pawn_sheet.png",
                combatUnit=combat.CombatUnit(
                    name="pulgita",
                    baseHP=500,
                    baseAttack=85,
                    baseDefense=80,
                    baseSpatk=75,
                    baseSpdef=90,
                    baseSpeed=115,
                    move0=movelist.getRevolverDatos(),
                    move1=movelist.getCrash(),
                    move2=movelist.getRomperInterfazVisual(),
                    weaknesses=["unit"],
                    resists=[],
                    immunities=[],
                    types=["bug"]
                ),
                x=500,
                y=200,
                dialog=[
                    "el enemigo empieza a moverse extrañamente",
                    "el enemigo dice cosas que no tienen sentido"
                ]
            )
