import config
import pygame
import globVariables
import gamestate


def getButtonY():
    return config.WIN_HEIGHT - (config.WIN_HEIGHT/4)+config.BUTTON_MARGINS


def getButtonHeight():
    return (config.WIN_HEIGHT/4)-(config.BUTTON_MARGINS*2)


# TODO: corregir esto y crear un sistema para poder renerizar x cantidad de botones
def getButtonX(buttonCount):
    return 400


def getButtonWidth(buttonCount):
    return 200


def drawButtons():
    globVariables.DISPLAYSURF.blit(globVariables.bg, (0, 0))
    pygame.draw.rect(
        globVariables.DISPLAYSURF,
        (0, 0, 0),
        pygame.Rect(
            getButtonX(3),
            getButtonY(),
            getButtonWidth(3),
            getButtonHeight()
        )
    )
    textSurface = globVariables.font.render(
        "presione a para comenzar",
        False,
        (255, 255, 255)
    )
    globVariables.DISPLAYSURF.blit(
        textSurface,
        (getButtonX(3)+config.BUTTON_MARGINS, getButtonY())
    )


def menuWorldLoop():
    drawButtons()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_a:
                    gamestate.gameloop = "world"
                case pygame.K_d:
                    pass
        if event.type == pygame.constants.QUIT:
            gamestate.exitflag = True
