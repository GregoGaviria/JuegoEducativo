import menuEntries
import movelist
import combat
import pygame
import config
import globVariables
import gamestate
import unittest


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


class Player():
    def __init__(self):
        self.worldObject = WorldObject(
            0,
            0,
            "assets/plagio.png",
            lambda: None
        )

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

        self.combat = combat.CombatUnit(
            name="crasheador",
            baseHP=500,
            baseAttack=115,
            baseDefense=70,
            baseSpatk=110,
            baseSpdef=65,
            baseSpeed=65,
            move0=movelist.getCrash(),
            move1=movelist.getCrash(),
            move2=movelist.getCrash(),
            weaknesses=["system"],
            resists=["unit"],
            immunities=[],
            types=["irritating"]
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
        config.WIN_WIDTH/2-30,
        config.WIN_HEIGHT/2 - 30,
        "assets/placeholder-libro.jpg",
        libroInteractFunc
    )


def getEnemy():
    return Enemy()
