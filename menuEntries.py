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
    return 400


def getButtonWidth(buttonCount):
    return 200


# def drawButtons():
#     pygame.draw.rect(
#         globVariables.DISPLAYSURF,
#         (0, 0, 0),
#         pygame.Rect(
#             getButtonX(3),
#             getButtonY(),
#             getButtonWidth(3),
#             getButtonHeight()
#         )
#     )
#     textSurface = globVariables.font.render(
#         "presione a para comenzar",
#         False,
#         (255, 255, 255)
#     )
#     globVariables.DISPLAYSURF.blit(
#         textSurface,
#         (getButtonX(3)+config.BUTTON_MARGINS, getButtonY())
#     )


class Button():
    def __init__(self, function, texto, textcolor, color, pos):
        self.function = function
        self.texto = texto
        self.color = color
        self.baseRec = pygame.Rect(
            getButtonX(3),
            getButtonY(),
            getButtonWidth(3),
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
            (getButtonX(3)+config.BUTTON_MARGINS, getButtonY())
        )


def init():
    global mainMenuBackground
    mainMenuBackground = pygame.image.load("assets/background-placeholder.jpg")
    global buttons
    buttons = []


def mainMenu():
    globVariables.DISPLAYSURF.blit(mainMenuBackground, (0, 0))


def loadMainMenu():
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
    pass
