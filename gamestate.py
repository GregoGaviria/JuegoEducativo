import pygame
import documentPages
import worldObjects
import islands
import globVariables


def init():
    global gameloop
    gameloop = "menu"
    global exitflag
    exitflag = False
    global player
    player = worldObjects.Player()
    global menuRenderLoop
    global document
    document = documentPages.getLibro()
    global buttons
    buttons = []
    global currentBattle

    # mundo dividido en 3 islas. cada una tiene su propio worldObjectList
    # que se conserva entre visitas (enemigos derrotados no reaparecen).
    global _islands
    _islands = islands.build()
    global currentIsland
    currentIsland = 0
    global worldObjectList
    worldObjectList = _islands[currentIsland]["objects"]
    global worldBackground
    worldBackground = _loadBackground(_islands[currentIsland]["background"])

    spawn = _islands[currentIsland]["defaultSpawn"]
    player.worldObject.rect.x = spawn[0]
    player.worldObject.rect.y = spawn[1]


def _loadBackground(path):
    surf = pygame.image.load(path).convert()
    return pygame.transform.scale(
        surf,
        globVariables.DISPLAYSURF.get_size()
    )


def loadIsland(idx, spawn=None):
    global currentIsland, worldObjectList, worldBackground
    currentIsland = idx
    worldObjectList = _islands[idx]["objects"]
    worldBackground = _loadBackground(_islands[idx]["background"])
    if spawn is None:
        spawn = _islands[idx]["defaultSpawn"]
    player.worldObject.rect.x = spawn[0]
    player.worldObject.rect.y = spawn[1]
