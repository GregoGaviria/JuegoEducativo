import menuEntries
import pygame
import config
import globVariables
import gamestate
import unittest
import random
import math


class WorldObject():
    def __init__(self, x, y, spritePath, interactFunc):
        self.sprite = pygame.transform.scale(
            pygame.image.load(spritePath),
            (64, 64)
        )
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.interactFunc = interactFunc

    def draw(self):
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


class Move():
    def __init__(
        self,
        moveName,
        desc,
        moveBP,
        moveACC,
        moveType,
        effect,
        special
    ):
        self.name = moveName
        self.bp = moveBP
        self.acc = moveACC
        self.type = moveType
        self.effect = effect
        self.desc = desc
        self.special = special

    def use(self, target, user):
        def applyBoost(stat, boost, denominator):
            multiplier = 1
            if boost > 6:
                boost = 6
                multiplier = ((denominator+boost)/denominator)
            elif boost < -6:
                boost = -6
                multiplier = (denominator/(denominator-boost))
            elif boost < 0:
                multiplier = (denominator/(denominator-boost))
            elif boost > 0:
                multiplier = ((denominator+boost)/denominator)
            return multiplier*stat
        battleLog = []

        accStat = applyBoost(self.acc, user.accuracy-target.evasion, 3)
        if accStat < random.randint(0, 100):
            battleLog.append("el movimiento fallo!")
            return battleLog

        attackingStat = 0
        defendingStat = 0
        if self.special:
            attackingStat = applyBoost(user.SPATK, user.spatkBoost, 2)
            defendingStat = applyBoost(user.SPDEF, user.spdefBoost, 2)
        else:
            attackingStat = applyBoost(user.ATTACK, user.attackBoost, 2)
            defendingStat = applyBoost(user.DEFENSE, user.defenseBoost, 2)

        damage = self.bp*(attackingStat/defendingStat)
        damage = damage*(random.randint(85, 100)/100)
        if 100-config.CRIT_CHANCE < random.randint(0, 100):
            battleLog.append("golpe critico!")
            damage = math.ceil(damage*1.5)

        target.hp = target.hp - damage

        battleLog = self.effect(target, user, battleLog)
        return battleLog


class Player():
    def __init__(self):
        self.worldObject = WorldObject(
            0,
            0,
            "assets/plagio.png",
            lambda: None
        )

        self.MAXHP = 500
        self.hp = 500
        self.ATTACK = 100
        self.DEFENSE = 100
        self.SPATK = 100
        self.SPDEF = 100
        self.SPEED = 100

        self.attackBoost = 0
        self.defenseBoost = 0
        self.spatkBoost = 0
        self.spdefBoost = 0
        self.speedBoost = 0
        self.evasion = 0
        self.accuracy = 0

        self.move0 = Move(
            "Unit Test",
            "prueba de una unidad aislada, sin efecto adicional",
            130,
            65,
            "unit",
            lambda a, b, c: None,
            False
        )

        def reduceEvasion(target, user, battleLog):
            target.evasion = target.evasion-1
            battleLog.append("se redujo la evasión")
            return battleLog
        self.move1 = Move(
            "Integration test",
            "prueba para multiples componentes, reduce evasión de enemigo",
            55,
            85,
            "integration",
            reduceEvasion,
            False
        )

        def reduce2selfAttack(target, user, battleLog):
            user.spatkBoost = user.spatkBoost-2
            battleLog.append("se redujo el ataque especial")
            return battleLog
        self.move2 = Move(
            "system test",
            "prueba de sistema completo, reduce tu propio ataque",
            190,
            85,
            "integration",
            reduce2selfAttack,
            True
        )

    def draw(self):
        self.worldObject.draw()


class Enemy():
    def __init__(self):
        def iniciateBattle():
            menuEntries.loadBattleMenu()
            gamestate.gameloop = "menu"
        self.worldObject = WorldObject(
            300,
            300,
            "assets/placeholder-enemigo.png",
            iniciateBattle
        )
        self.MAXHP = 500
        self.hp = 500
        self.ATTACK = 115
        self.DEFENSE = 70
        self.SPATK = 110
        self.SPDEF = 65
        self.SPEED = 65

        self.attackBoost = 0
        self.defenseBoost = 0
        self.spatkBoost = 0
        self.spdefBoost = 0
        self.speedBoost = 0
        self.evasion = 0
        self.accuracy = 0

    def draw(self):
        self.worldObject.draw()

    def playerwithinrange(self):
        self.worldObject.playerwithinrange()


def getLibro():
    def libroInteractFunc():
        menuEntries.loadBookMenu()
        gamestate.gameloop = "menu"
    return WorldObject(
        config.WIN_WIDTH/2-30,
        config.WIN_HEIGHT/2 - 30,
        "assets/placeholder-libro.jpg",
        libroInteractFunc
    )


def getEnemy():
    return Enemy()
