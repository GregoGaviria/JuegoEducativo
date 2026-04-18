import pygame
import globVariables
import gamestate
import config
import worldObjects


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


def loadMainMenu():
    mainMenuBackground = pygame.image.load("assets/background-placeholder.jpg")

    def renderLoop():
        globVariables.DISPLAYSURF.blit(mainMenuBackground, (0, 0))
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        gamestate.gameloop = "world"
    button0 = Button(
        button0func,
        "Presione U para comenzar",
        (255, 255, 255),
        (0, 0, 0),
        0
    )
    gamestate.buttons.append(button0)

    def button1func():
        pass
    button1 = Button(
        button1func,
        "",
        (255, 255, 255),
        (0, 0, 0),
        1
    )
    gamestate.buttons.append(button1)

    def button2func():
        pass
    button2 = Button(
        button2func,
        "",
        (255, 255, 255),
        (0, 0, 0),
        2
    )
    gamestate.buttons.append(button2)

    def button3func():
        gamestate.exitflag = True
    button3 = Button(
        button3func,
        "Cerrar juego",
        (255, 255, 255),
        (0, 0, 0),
        3
    )
    gamestate.buttons.append(button3)


def loadBookMenu():
    def renderLoop():
        globVariables.DISPLAYSURF.blit(gamestate.document.background, (0, 0))
        gamestate.document.render()
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        gamestate.document.prevPage()
    button0 = Button(
        button0func,
        "pagina anterior",
        (255, 255, 255),
        (0, 0, 0),
        0
    )
    gamestate.buttons.append(button0)

    def button1func():
        pass
    button1 = Button(
        button1func,
        "",
        (255, 255, 255),
        (0, 0, 0),
        1
    )
    gamestate.buttons.append(button1)

    def button2func():
        gamestate.document.nextPage()
    button2 = Button(
        button2func,
        "proxima pagina",
        (255, 255, 255),
        (0, 0, 0),
        2
    )
    gamestate.buttons.append(button2)

    def button3func():
        gamestate.gameloop = "world"
    button3 = Button(
        button3func,
        "Salir",
        (255, 255, 255),
        (0, 0, 0),
        3
    )
    gamestate.buttons.append(button3)


def loadBattleMenu():
    background = pygame.transform.scale(
        pygame.image.load("assets/background-placeholder.jpg"),
        (config.WIN_WIDTH, config.WIN_HEIGHT)
    )
    enemySprite = pygame.transform.scale(
        pygame.image.load("assets/placeholder-enemigo.png"),
        (400, 400)
    )
    enemy = worldObjects.getEnemy()

    def renderLoop():
        globVariables.DISPLAYSURF.blit(background, (0, 0))
        globVariables.DISPLAYSURF.blit(enemySprite, (40, 40))
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        print(gamestate.player.combat.move0.use(
            enemy.combat, gamestate.player.combat))
        print(enemy.combat.hp)
        print("bastos")
    button0 = Button(
        button0func,
        "Movimiento 1",
        (255, 255, 255),
        (0, 0, 0),
        0
    )
    gamestate.buttons.append(button0)

    def button1func():
        print(gamestate.player.combat.move1.use(
            enemy.combat, gamestate.player.combat))
        print(enemy.combat.hp)
        print("bastos")
    button1 = Button(
        button1func,
        "Movimiento 2",
        (255, 255, 255),
        (0, 0, 0),
        1
    )
    gamestate.buttons.append(button1)

    def button2func():
        print(gamestate.player.combat.move2.use(
            enemy.combat, gamestate.player.combat))
        print(enemy.combat.hp)
        print("bastos")
    button2 = Button(
        button2func,
        "Movimiento 3",
        (255, 255, 255),
        (0, 0, 0),
        2
    )
    gamestate.buttons.append(button2)

    def button3func():
        # gamestate.player.move0()
        gamestate.gameloop = "world"
    button3 = Button(
        button3func,
        "Movimiento 4",
        (255, 255, 255),
        (0, 0, 0),
        3
    )
    gamestate.buttons.append(button3)
