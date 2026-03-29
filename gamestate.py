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
    document = documentPages.Document(
        [
            [
                "la primera linea de texto, primera pagina",
                "la segunda linea de texto, primera pagina",
                "la tercera linea de texto, primera pagina",
            ],
            [
                "la primera linea de texto, segunda pagina",
                "la segunda linea de texto, segunda pagina",
                "la tercera linea de texto, segunda pagina",
            ],
            [
                "la primera linea de texto, tercera pagina",
                "la segunda linea de texto, tercera pagina",
                "la tercera linea de texto, tercera pagina",
            ],
        ],
        (255,0,0),
        "assets/background-placeholder.jpg"
    )
