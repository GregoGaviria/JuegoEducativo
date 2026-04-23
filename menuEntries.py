import combat
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


def hpBarLengthCalc(unit):
    if unit.hp <= 0:
        return 0
    return (unit.hp/(unit.MAXHP/100))/100


def loadBattleMenu(enemy):
    gamestate.currentBattle = combat.Battle(enemy)
    background = pygame.transform.scale(
        pygame.image.load("assets/background-placeholder.jpg"),
        (config.WIN_WIDTH, config.WIN_HEIGHT)
    )
    enemySprite = enemy.getCombatSprite()
    textSurface = globVariables.font.render(
        "empieza el combate con "+enemy.combat.name,
        False,
        (255, 255, 255)
    )
    textRectangle = pygame.Rect(
        50,
        450,
        config.WIN_WIDTH-100,
        50,
    )

    def renderLoop():
        globVariables.DISPLAYSURF.blit(background, (0, 0))
        globVariables.DISPLAYSURF.blit(enemySprite, (40, 40))
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            textRectangle
        )
        globVariables.DISPLAYSURF.blit(
            textSurface,
            (
                textRectangle.x+config.BUTTON_MARGINS,
                textRectangle.y+config.BUTTON_MARGINS
            )
        )
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        LoadTurnMenu(enemy)
    button0 = Button(
        button0func,
        "Movimiento 1",
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
        gamestate.gameloop = "world"
    button3 = Button(
        button3func,
        "Salir",
        (255, 255, 255),
        (0, 0, 0),
        3
    )
    gamestate.buttons.append(button3)


def LoadTurnMenu(enemy):
    gamestate.currentBattle = combat.Battle(enemy)
    background = pygame.transform.scale(
        pygame.image.load("assets/background-placeholder.jpg"),
        (config.WIN_WIDTH, config.WIN_HEIGHT)
    )
    enemySprite = enemy.getCombatSprite()
    textSurface = globVariables.font.render(
        enemy.getRandomDialog(),
        False,
        (255, 255, 255)
    )
    textRectangle = pygame.Rect(
        50,
        450,
        config.WIN_WIDTH-100,
        50,
    )
    barLabelEnemy = globVariables.font.render(
        enemy.combat.name+": ",
        False,
        (255, 255, 255)
    )
    hpBarBackgroundEnemy = pygame.Rect(
        50,
        500,
        config.WIN_WIDTH-100,
        50,
    )
    hpBarWhiteEnemy = pygame.Rect(
        150,
        510,
        config.WIN_WIDTH-220,
        30,
    )
    hpBarRedEnemy = pygame.Rect(
        153,
        513,
        (config.WIN_WIDTH-226)*hpBarLengthCalc(enemy.combat),
        24
    )
    hpbarBlackEnemy = pygame.Rect(
        153,
        513,
        config.WIN_WIDTH-226,
        24
    )

    barLabelPlayer = globVariables.font.render(
        "Jugador: ",
        False,
        (255, 255, 255)
    )
    hpBarBackgroundPlayer = pygame.Rect(
        50,
        550,
        config.WIN_WIDTH-100,
        50,
    )
    hpBarWhitePlayer = pygame.Rect(
        150,
        560,
        config.WIN_WIDTH-220,
        30,
    )
    hpBarGreenPlayer = pygame.Rect(
        153,
        563,
        (config.WIN_WIDTH-226)*hpBarLengthCalc(gamestate.player.combat),
        24
    )
    hpbarBlackPlayer = pygame.Rect(
        153,
        563,
        config.WIN_WIDTH-226,
        24
    )

    def renderLoop():
        globVariables.DISPLAYSURF.blit(background, (0, 0))
        globVariables.DISPLAYSURF.blit(enemySprite, (40, 40))
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            textRectangle
        )
        globVariables.DISPLAYSURF.blit(
            textSurface,
            (
                textRectangle.x+config.BUTTON_MARGINS,
                textRectangle.y+config.BUTTON_MARGINS
            )
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpBarBackgroundEnemy
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (255, 255, 255),
            hpBarWhiteEnemy
        )
        globVariables.DISPLAYSURF.blit(
            barLabelEnemy,
            (
                hpBarBackgroundEnemy.x+config.BUTTON_MARGINS,
                hpBarBackgroundEnemy.y+config.BUTTON_MARGINS+10
            )
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpBarBackgroundPlayer
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (255, 255, 255),
            hpBarWhitePlayer
        )
        globVariables.DISPLAYSURF.blit(
            barLabelPlayer,
            (
                hpBarBackgroundPlayer.x+config.BUTTON_MARGINS,
                hpBarBackgroundPlayer.y+config.BUTTON_MARGINS+10
            )
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpbarBlackPlayer
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpbarBlackEnemy
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 255, 0),
            hpBarGreenPlayer
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (255, 0, 0),
            hpBarRedEnemy
        )
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    # def handleResults(results):
    #     if results["vFlag"]:
    #         pass
    #     if results["lFlag"]:
    #         pass

    def button0func():
        LoadLogMenu(
            enemy,
            combat.initTurn(
                gamestate.player.combat.move0,
                gamestate.player.combat,
                enemy.combat
            ))
    button0 = Button(
        button0func,
        "Movimiento 1",
        (255, 255, 255),
        (0, 0, 0),
        0
    )
    gamestate.buttons.append(button0)

    def button1func():
        LoadLogMenu(
            enemy,
            combat.initTurn(
                gamestate.player.combat.move1,
                gamestate.player.combat,
                enemy.combat
            ))
    button1 = Button(
        button1func,
        "Movimiento 2",
        (255, 255, 255),
        (0, 0, 0),
        1
    )
    gamestate.buttons.append(button1)

    def button2func():
        LoadLogMenu(
            enemy,
            combat.initTurn(
                gamestate.player.combat.move2,
                gamestate.player.combat,
                enemy.combat
            ))
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


def LoadLogMenu(enemy, log):
    gamestate.currentBattle = combat.Battle(enemy)
    background = pygame.transform.scale(
        pygame.image.load("assets/background-placeholder.jpg"),
        (config.WIN_WIDTH, config.WIN_HEIGHT)
    )
    enemySprite = enemy.getCombatSprite()
    textSurface = globVariables.font.render(
        log[0],
        False,
        (255, 255, 255)
    )
    textRectangle = pygame.Rect(
        50,
        450,
        config.WIN_WIDTH-100,
        50,
    )
    barLabelEnemy = globVariables.font.render(
        enemy.combat.name+": ",
        False,
        (255, 255, 255)
    )
    hpBarBackgroundEnemy = pygame.Rect(
        50,
        500,
        config.WIN_WIDTH-100,
        50,
    )
    hpBarWhiteEnemy = pygame.Rect(
        150,
        510,
        config.WIN_WIDTH-220,
        30,
    )
    hpBarRedEnemy = pygame.Rect(
        153,
        513,
        (config.WIN_WIDTH-226)*hpBarLengthCalc(enemy.combat),
        24
    )
    hpbarBlackEnemy = pygame.Rect(
        153,
        513,
        config.WIN_WIDTH-226,
        24
    )

    barLabelPlayer = globVariables.font.render(
        "Jugador: ",
        False,
        (255, 255, 255)
    )
    hpBarBackgroundPlayer = pygame.Rect(
        50,
        550,
        config.WIN_WIDTH-100,
        50,
    )
    hpBarWhitePlayer = pygame.Rect(
        150,
        560,
        config.WIN_WIDTH-220,
        30,
    )
    hpBarGreenPlayer = pygame.Rect(
        153,
        563,
        (config.WIN_WIDTH-226)*hpBarLengthCalc(gamestate.player.combat),
        24
    )
    hpbarBlackPlayer = pygame.Rect(
        153,
        563,
        config.WIN_WIDTH-226,
        24
    )

    def renderLoop():
        globVariables.DISPLAYSURF.blit(background, (0, 0))
        globVariables.DISPLAYSURF.blit(enemySprite, (40, 40))
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            textRectangle
        )
        globVariables.DISPLAYSURF.blit(
            textSurface,
            (
                textRectangle.x+config.BUTTON_MARGINS,
                textRectangle.y+config.BUTTON_MARGINS
            )
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpBarBackgroundEnemy
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (255, 255, 255),
            hpBarWhiteEnemy
        )
        globVariables.DISPLAYSURF.blit(
            barLabelEnemy,
            (
                hpBarBackgroundEnemy.x+config.BUTTON_MARGINS,
                hpBarBackgroundEnemy.y+config.BUTTON_MARGINS+10
            )
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpBarBackgroundPlayer
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (255, 255, 255),
            hpBarWhitePlayer
        )
        globVariables.DISPLAYSURF.blit(
            barLabelPlayer,
            (
                hpBarBackgroundPlayer.x+config.BUTTON_MARGINS,
                hpBarBackgroundPlayer.y+config.BUTTON_MARGINS+10
            )
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpbarBlackPlayer
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 0, 0),
            hpbarBlackEnemy
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (0, 255, 0),
            hpBarGreenPlayer
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (255, 0, 0),
            hpBarRedEnemy
        )
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        if len(log) == 1:
            LoadTurnMenu(enemy)
        else:
            LoadLogMenu(enemy, log[1:])

    button0 = Button(
        button0func,
        "Movimiento 1",
        (255, 255, 255),
        (0, 0, 0),
        0
    )
    gamestate.buttons.append(button0)

    def button1func():
        pass
    button1 = Button(
        button1func,
        "Movimiento 2",
        (255, 255, 255),
        (0, 0, 0),
        1
    )
    gamestate.buttons.append(button1)

    def button2func():
        pass
    button2 = Button(
        button2func,
        "Movimiento 3",
        (255, 255, 255),
        (0, 0, 0),
        2
    )
    gamestate.buttons.append(button2)

    def button3func():
        gamestate.gameloop = "world"
    button3 = Button(
        button3func,
        "Movimiento 4",
        (255, 255, 255),
        (0, 0, 0),
        3
    )
    gamestate.buttons.append(button3)
