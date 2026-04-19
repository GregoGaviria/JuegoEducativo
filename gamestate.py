import documentPages
import worldObjects
# import combat


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
    global currentBattle
    worldObjectList.append(worldObjects.getLibro())
    worldObjectList.append(worldObjects.getEnemy("crasheador"))
    worldObjectList.append(worldObjects.getEnemy("conexion"))
