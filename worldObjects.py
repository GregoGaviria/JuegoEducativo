import menuEntries
import pygame
import config
import globVariables
import gamestate


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
        self.worldObject = WorldObject(0, 0, "assets/plagio.png", lambda: None)

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
