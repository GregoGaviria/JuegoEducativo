import documentPages
import worldObjects


def init():
    global gameloop
    gameloop = "menu"
    global exitflag
    exitflag = False
    global player
    player = worldObjects.Player()
    global menuRenderLoop
    # currentMenu = menuEntries.mainMenu
    global document
    document = documentPages.getLibro()
    global worldObjectList
    worldObjectList = []
    global buttons
    buttons = []
    worldObjectList.append(worldObjects.getLibro())
    worldObjectList.append(worldObjects.getEnemy())
