import menuEntries
import documentPages
import worldObjects


def init():
    global gameloop
    gameloop = "menu"
    global exitflag
    exitflag = False
    global player
    player = worldObjects.Player()
    global currentMenu
    currentMenu = menuEntries.mainMenu
    global document
    document = documentPages.getLibro()
    global worldObjectList
    worldObjectList = []
    worldObjectList.append(worldObjects.getLibro())
    worldObjectList.append(worldObjects.getEnemy())
