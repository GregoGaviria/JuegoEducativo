import menuEntries
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
