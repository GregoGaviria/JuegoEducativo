import pygame
import globVariables
import gamestate
import config


def getButtonY():
    return config.WIN_HEIGHT - (config.WIN_HEIGHT/4)+config.BUTTON_MARGINS


def getButtonHeight():
    return (config.WIN_HEIGHT/4)-(config.BUTTON_MARGINS*2)


# TODO: corregir esto y crear un sistema para poder renerizar x cantidad de botones
def getButtonX(buttonCount):
    return ((config.WIN_WIDTH/4)*buttonCount)+config.BUTTON_MARGINS


def getButtonWidth():
    return (config.WIN_WIDTH/4)-(config.BUTTON_MARGINS*2)


class Button():
    def __init__(self, function, texto, textcolor, color, pos):
        self.function = function
        self.texto = texto
        self.color = color
        self.baseRec = pygame.Rect(
            getButtonX(pos),
            getButtonY(),
            getButtonWidth(),
            getButtonHeight()
        )
        self.textSurface = globVariables.font.render(
            self.texto,
            False,
            textcolor
        )

    def render(self):
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            self.color,
            self.baseRec
        )
        globVariables.DISPLAYSURF.blit(
            self.textSurface,
            (self.baseRec.x+config.BUTTON_MARGINS,
             self.baseRec.y+config.BUTTON_MARGINS)
        )


def init():
    global mainMenuBackground
    mainMenuBackground = pygame.image.load("assets/background-placeholder.jpg")
    global buttons
    buttons = []


def mainMenu():
    globVariables.DISPLAYSURF.blit(mainMenuBackground, (0, 0))


def loadMainMenu():
    gamestate.currentMenu = mainMenu
    buttons.clear()

    def button0func():
        gamestate.gameloop = "world"
    button0 = Button(
        button0func,
        "Presione U para comenzar",
        (255, 255, 255),
        (0, 0, 0),
        0
    )
    buttons.append(button0)

    def button1func():
        pass
    button1 = Button(
        button1func,
        "",
        (255, 255, 255),
        (0, 0, 0),
        1
    )
    buttons.append(button1)

    def button2func():
        pass
    button2 = Button(
        button2func,
        "",
        (255, 255, 255),
        (0, 0, 0),
        2
    )
    buttons.append(button2)

    def button3func():
        gamestate.exitflag = True
    button3 = Button(
        button3func,
        "Cerrar juego",
        (255, 255, 255),
        (0, 0, 0),
        3
    )
    buttons.append(button3)


def bookMenu():
    globVariables.DISPLAYSURF.blit(gamestate.document.background, (0, 0))
    gamestate.document.render()


def loadBookMenu():
    gamestate.currentMenu = bookMenu
    buttons.clear()

    def button0func():
        gamestate.document.prevPage()
    button0 = Button(
        button0func,
        "pagina anterior",
        (255, 255, 255),
        (0, 0, 0),
        0
    )
    buttons.append(button0)

    def button1func():
        pass
    button1 = Button(
        button1func,
        "",
        (255, 255, 255),
        (0, 0, 0),
        1
    )
    buttons.append(button1)

    def button2func():
        gamestate.document.nextPage()
    button2 = Button(
        button2func,
        "proxima pagina",
        (255, 255, 255),
        (0, 0, 0),
        2
    )
    buttons.append(button2)

    def button3func():
        gamestate.gameloop="world"
    button3 = Button(
        button3func,
        "Salir",
        (255, 255, 255),
        (0, 0, 0),
        3
    )
    buttons.append(button3)
