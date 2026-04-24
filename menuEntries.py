import combat
import pygame
import globVariables
import gamestate
import config
import worldObjects
import combatSprites
import audio
import transition
import particles


# posicionamiento de los sprites en combate
PLAYER_SPRITE_POS = (40, 360)
ENEMY_SPRITE_POS = (536, 40)
# jefe: mas grande, centrado para que se vea imponente
BOSS_SPRITE_POS = (348, 0)
COMBAT_SPRITE_SIZE = 320
BOSS_SPRITE_SIZE = 560

# flash dorado de "iluminacion de ultima hora": se activa cuando el
# jugador baja de 100 hp en la bossfight y reporta el evento por log
_enlightenmentFlashStart = 0
_ENLIGHTENMENT_DURATION = 1500


def _drawHpBar(label, unit, x, y, width, fillColor):
    # marco de madera
    border = pygame.Rect(x, y, width, 34)
    pygame.draw.rect(
        globVariables.DISPLAYSURF, (60, 40, 20), border, border_radius=6
    )
    pygame.draw.rect(
        globVariables.DISPLAYSURF, (210, 180, 120), border, 2, border_radius=6
    )
    # fondo interno oscuro
    inner = pygame.Rect(x+4, y+4, width-8, 26)
    pygame.draw.rect(
        globVariables.DISPLAYSURF, (30, 20, 10), inner, border_radius=4
    )
    # relleno proporcional a hp
    ratio = max(0, unit.hp) / unit.MAXHP
    fillWidth = int((width-8) * ratio)
    if fillWidth > 0:
        fill = pygame.Rect(x+4, y+4, fillWidth, 26)
        pygame.draw.rect(
            globVariables.DISPLAYSURF, fillColor, fill, border_radius=4
        )
    # etiqueta
    txt = globVariables.font.render(
        label + "  " + str(max(0, unit.hp)) + "/" + str(unit.MAXHP),
        True,
        (255, 255, 255)
    )
    globVariables.DISPLAYSURF.blit(txt, (x+10, y+8))


def _drawCombatScene(enemy, message):
    # fondo distinto para el jefe (mas oscuro y dramatico)
    isBoss = getattr(enemy, "isBoss", False)
    bg = globVariables.bossBattleBackground if isBoss else (
        globVariables.menuBackground
    )
    globVariables.DISPLAYSURF.blit(bg, (0, 0))
    # sprites animados (el jefe se posiciona mas centrado y grande)
    enemyPos = BOSS_SPRITE_POS if isBoss else ENEMY_SPRITE_POS
    gamestate.enemyCombatSprite.draw(
        globVariables.DISPLAYSURF, *enemyPos
    )
    gamestate.playerCombatSprite.draw(
        globVariables.DISPLAYSURF, *PLAYER_SPRITE_POS
    )
    # barra de vida del enemigo arriba izquierda
    _drawHpBar(
        enemy.combat.name, enemy.combat,
        40, 40, 400, (220, 60, 60)
    )
    # barra de vida del jugador abajo derecha
    _drawHpBar(
        "jugador", gamestate.player.combat,
        config.WIN_WIDTH-440, 400, 400, (60, 200, 80)
    )
    # chispas del impacto encima de los sprites
    particles.updateBursts()
    particles.drawBursts()
    # flash dorado de iluminacion por encima de todo: fade out suave
    if _enlightenmentFlashStart > 0:
        elapsed = pygame.time.get_ticks() - _enlightenmentFlashStart
        if elapsed < _ENLIGHTENMENT_DURATION:
            t = 1 - (elapsed / _ENLIGHTENMENT_DURATION)
            flash = pygame.Surface(
                (config.WIN_WIDTH, config.WIN_HEIGHT), pygame.SRCALPHA
            )
            flash.fill((255, 230, 140, int(180 * t)))
            globVariables.DISPLAYSURF.blit(flash, (0, 0))
    # caja de mensaje
    msgRect = pygame.Rect(40, 560, config.WIN_WIDTH-80, 64)
    pygame.draw.rect(
        globVariables.DISPLAYSURF, (20, 15, 10), msgRect, border_radius=6
    )
    pygame.draw.rect(
        globVariables.DISPLAYSURF, (210, 180, 120), msgRect, 2, border_radius=6
    )
    msgFont = pygame.font.SysFont("Noto Sans", 20)
    msgSurf = msgFont.render(message, True, (255, 255, 255))
    globVariables.DISPLAYSURF.blit(
        msgSurf, (msgRect.x+16, msgRect.y+20)
    )


def _triggerAttackFromLog(enemy, logLine):
    # dispara la animacion de ataque + SFX de espada segun el log
    # + particulas en el impacto para darle peso al golpe
    if logLine.startswith(gamestate.player.combat.name + " utiliza"):
        gamestate.playerCombatSprite.startAttack()
        audio.playSlash()
        # el enemigo recibe el golpe: chispas en su centro
        enemyPos = BOSS_SPRITE_POS if getattr(enemy, "isBoss", False) else ENEMY_SPRITE_POS
        esize = BOSS_SPRITE_SIZE if getattr(enemy, "isBoss", False) else COMBAT_SPRITE_SIZE
        particles.spawnBurst(
            enemyPos[0] + esize // 2,
            enemyPos[1] + esize // 2,
            count=18,
            color=(255, 220, 120)
        )
    elif logLine.startswith(enemy.combat.name + " utiliza"):
        gamestate.enemyCombatSprite.startAttack()
        audio.playSlash()
        particles.spawnBurst(
            PLAYER_SPRITE_POS[0] + COMBAT_SPRITE_SIZE // 2,
            PLAYER_SPRITE_POS[1] + COMBAT_SPRITE_SIZE // 2,
            count=14,
            color=(255, 120, 120)
        )
    elif logLine == "el movimiento es super effectivo!":
        audio.playSuperEffective()
    elif logLine == "iluminacion de ultima hora!":
        # flash dorado a pantalla completa + rafaga de particulas
        # alrededor del jugador, mas el SFX de golpe especial
        global _enlightenmentFlashStart
        _enlightenmentFlashStart = pygame.time.get_ticks()
        cx = PLAYER_SPRITE_POS[0] + COMBAT_SPRITE_SIZE // 2
        cy = PLAYER_SPRITE_POS[1] + COMBAT_SPRITE_SIZE // 2
        particles.spawnBurst(cx, cy, count=60, color=(255, 240, 160))
        particles.spawnBurst(cx, cy, count=30, color=(255, 210, 80))
        audio.playSuperEffective()
    elif logLine == "la iluminacion protege al jugador!":
        # rafaga dorada mas pequena cada vez que absorbe un golpe
        cx = PLAYER_SPRITE_POS[0] + COMBAT_SPRITE_SIZE // 2
        cy = PLAYER_SPRITE_POS[1] + COMBAT_SPRITE_SIZE // 2
        particles.spawnBurst(cx, cy, count=20, color=(255, 230, 140))


def getButtonY():
    return config.WIN_HEIGHT - (config.WIN_HEIGHT/4)+config.BUTTON_MARGINS


def getButtonHeight():
    return (config.WIN_HEIGHT/4)-(config.BUTTON_MARGINS*2)


# TODO: corregir esto y crear un sistema para poder renerizar x cantidad de botones
def getButtonX(buttonCount):
    return ((config.WIN_WIDTH/4)*buttonCount)+config.BUTTON_MARGINS


def getButtonWidth():
    return (config.WIN_WIDTH/4)-(config.BUTTON_MARGINS*2)


BUTTON_KEYS = ["U", "I", "O", "P"]


class Button():
    def __init__(self, function, texto, textcolor, color, pos):
        self.function = function
        self.texto = texto
        self.color = color
        self.pos = pos
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
        # etiqueta de la tecla (ej: "[U]") arriba a la izquierda del boton
        self.keySurface = globVariables.buttonKeyFont.render(
            "[" + BUTTON_KEYS[pos] + "]",
            True,
            (255, 220, 140)
        )

    def render(self):
        # botones sin texto no se dibujan (ranuras vacias)
        if self.texto == "":
            return
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            self.color,
            self.baseRec
        )
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (210, 180, 120),
            self.baseRec,
            2
        )
        # tecla arriba a la izquierda
        globVariables.DISPLAYSURF.blit(
            self.keySurface,
            (self.baseRec.x+config.BUTTON_MARGINS,
             self.baseRec.y+config.BUTTON_MARGINS)
        )
        # texto del boton, debajo de la tecla
        globVariables.DISPLAYSURF.blit(
            self.textSurface,
            (self.baseRec.x+config.BUTTON_MARGINS,
             self.baseRec.y+config.BUTTON_MARGINS +
             self.keySurface.get_height() + 6)
        )


def loadGameOverMenu():
    # fondo negro con titulo rojo imponente y subtitulo
    gamestate.buttons.clear()
    titleFont = pygame.font.SysFont("Noto Sans", 120, bold=True)
    subFont = pygame.font.SysFont("Noto Sans", 28, italic=True)
    titleMain = titleFont.render("GAME OVER", True, (200, 30, 30))
    titleShadow = titleFont.render("GAME OVER", True, (40, 0, 0))
    subtitle = subFont.render(
        "los bugs te vencieron...", True, (220, 200, 200)
    )

    def renderLoop():
        globVariables.DISPLAYSURF.fill((8, 4, 6))
        # viñeta roja suave
        vig = pygame.Surface(
            (config.WIN_WIDTH, config.WIN_HEIGHT), pygame.SRCALPHA
        )
        pygame.draw.circle(
            vig, (80, 10, 10, 80),
            (config.WIN_WIDTH // 2, config.WIN_HEIGHT // 2),
            config.WIN_WIDTH // 2
        )
        globVariables.DISPLAYSURF.blit(vig, (0, 0))
        tx = (config.WIN_WIDTH - titleMain.get_width()) // 2
        ty = 280
        # sombra desplazada para dar peso
        globVariables.DISPLAYSURF.blit(titleShadow, (tx + 6, ty + 6))
        globVariables.DISPLAYSURF.blit(titleMain, (tx, ty))
        sx = (config.WIN_WIDTH - subtitle.get_width()) // 2
        globVariables.DISPLAYSURF.blit(subtitle, (sx, ty + 150))
    gamestate.menuRenderLoop = renderLoop
    gamestate.gameloop = "menu"

    def button0func():
        # reinicia el juego: restaura HP del jugador, islas y spawn
        gamestate.player.combat.hp = gamestate.player.combat.MAXHP
        gamestate._islands[:] = __import__("islands").build()
        gamestate.loadIsland(0)
        audio.setWorldBgm(audio.ZELDA)
        audio.ensureWorldBgm()
        def exit():
            gamestate.gameloop = "world"
        transition.start(exit, duration=2000)
    gamestate.buttons.append(Button(
        button0func, "reintentar", (255, 255, 255), (32, 32, 32), 0
    ))
    gamestate.buttons.append(Button(
        lambda: None, "", (255, 255, 255), (0, 0, 0), 1
    ))
    gamestate.buttons.append(Button(
        lambda: None, "", (255, 255, 255), (0, 0, 0), 2
    ))

    def button3func():
        gamestate.exitflag = True
    gamestate.buttons.append(Button(
        button3func, "salir", (255, 255, 255), (32, 32, 32), 3
    ))


def loadMainMenu():
    titleFont = pygame.font.SysFont("Noto Sans", 64, bold=True)
    titleLine1 = titleFont.render(
        "juego educativo", True, (250, 240, 210)
    )
    titleLine2 = titleFont.render(
        "de pruebas de software", True, (250, 240, 210)
    )
    subtitleFont = pygame.font.SysFont("Noto Sans", 24, italic=True)
    subtitleSurface = subtitleFont.render(
        "aprende testing peleando bugs", True, (240, 230, 200)
    )
    # panel oscuro detras del titulo
    panelHeight = 260
    panel = pygame.Surface(
        (config.WIN_WIDTH - 80, panelHeight), pygame.SRCALPHA
    )
    panel.fill((20, 15, 10, 190))
    panelX = 40
    panelY = 180

    def renderLoop():
        globVariables.DISPLAYSURF.blit(globVariables.menuBackground, (0, 0))
        globVariables.DISPLAYSURF.blit(panel, (panelX, panelY))
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (210, 180, 120),
            (panelX, panelY, config.WIN_WIDTH - 80, panelHeight),
            3
        )
        t1x = (config.WIN_WIDTH - titleLine1.get_width())/2
        globVariables.DISPLAYSURF.blit(titleLine1, (t1x, panelY + 30))
        t2x = (config.WIN_WIDTH - titleLine2.get_width())/2
        globVariables.DISPLAYSURF.blit(titleLine2, (t2x, panelY + 100))
        sx = (config.WIN_WIDTH - subtitleSurface.get_width())/2
        globVariables.DISPLAYSURF.blit(subtitleSurface, (sx, panelY + 200))
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        gamestate.gameloop = "world"
    button0 = Button(
        button0func,
        "Presione U para comenzar",
        (255, 255, 255),
        (32, 32, 32),
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
        (32, 32, 32),
        3
    )
    gamestate.buttons.append(button3)


def loadBookMenu():
    def renderLoop():
        gamestate.document.render()
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        gamestate.document.prevPage()
    button0 = Button(
        button0func,
        "pagina anterior",
        (255, 255, 255),
        (32, 32, 32),
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
        (32, 32, 32),
        2
    )
    gamestate.buttons.append(button2)

    def button3func():
        gamestate.gameloop = "world"
    button3 = Button(
        button3func,
        "Salir",
        (255, 255, 255),
        (32, 32, 32),
        3
    )
    gamestate.buttons.append(button3)


def hpBarLengthCalc(unit):
    if unit.hp <= 0:
        return 0
    return (unit.hp/(unit.MAXHP/100))/100


def loadBattleMenu(enemy):
    gamestate.currentBattle = combat.Battle(enemy)
    # la musica de combate ya la arranco Enemy.iniciateBattle antes de
    # la transicion (main o final segun sea jefe), asi que aqui no
    # volvemos a pisarla
    # reset de iluminacion por combate: se gasta en bossfight solamente
    gamestate.player.combat.enlightenmentUsed = False
    gamestate.player.combat.immunityCharges = 0
    global _enlightenmentFlashStart
    _enlightenmentFlashStart = 0
    # el jefe se dibuja mas grande en combate para que se vea imponente
    bossBigger = getattr(enemy, "isBoss", False)
    enemySize = BOSS_SPRITE_SIZE if bossBigger else COMBAT_SPRITE_SIZE
    gamestate.playerCombatSprite = combatSprites.forPlayer(
        size=COMBAT_SPRITE_SIZE
    )
    gamestate.enemyCombatSprite = combatSprites.forEnemy(
        enemy, size=enemySize
    )

    def renderLoop():
        _drawCombatScene(
            enemy, "empieza el combate con " + enemy.combat.name
        )
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        LoadTurnMenu(enemy)
    gamestate.buttons.append(Button(
        button0func, "comenzar", (255, 255, 255), (32, 32, 32), 0
    ))
    gamestate.buttons.append(Button(
        lambda: None, "", (255, 255, 255), (0, 0, 0), 1
    ))
    gamestate.buttons.append(Button(
        lambda: None, "", (255, 255, 255), (0, 0, 0), 2
    ))

    def button3func():
        # vuelve la musica del mundo ya, asi suena durante la transicion
        audio.ensureWorldBgm()
        def exit():
            gamestate.gameloop = "world"
        transition.start(exit, duration=2500)
    gamestate.buttons.append(Button(
        button3func, "salir", (255, 255, 255), (32, 32, 32), 3
    ))


def LoadTurnMenu(enemy):
    gamestate.currentBattle = combat.Battle(enemy)
    message = "elegi un movimiento"

    def renderLoop():
        _drawCombatScene(enemy, message)
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def makeMoveFunc(move):
        def fn():
            LoadLogMenu(
                enemy,
                combat.initTurn(move, gamestate.player.combat, enemy.combat)
            )
        return fn

    gamestate.buttons.append(Button(
        makeMoveFunc(gamestate.player.combat.move0),
        gamestate.player.combat.move0.name,
        (255, 255, 255), (128, 32, 32), 0
    ))
    gamestate.buttons.append(Button(
        makeMoveFunc(gamestate.player.combat.move1),
        gamestate.player.combat.move1.name,
        (255, 255, 255), (32, 128, 32), 1
    ))
    gamestate.buttons.append(Button(
        makeMoveFunc(gamestate.player.combat.move2),
        gamestate.player.combat.move2.name,
        (255, 255, 255), (32, 32, 128), 2
    ))

    def button3func():
        # vuelve la musica del mundo ya, asi suena durante la transicion
        audio.ensureWorldBgm()
        def exit():
            gamestate.gameloop = "world"
        transition.start(exit, duration=2500)
    gamestate.buttons.append(Button(
        button3func, "salir", (255, 255, 255), (32, 32, 32), 3
    ))


def LoadLogMenu(enemy, log):
    gamestate.currentBattle = combat.Battle(enemy)
    # si la linea actual del log es "X utiliza movimiento Y", lanzar la
    # animacion de ataque del correspondiente sprite
    _triggerAttackFromLog(enemy, log[0])
    message = log[0]
    # si ya es la ultima linea de victoria, arrancamos el tema de victoria
    # aca mismo (a un "siguiente" de salir) y dejamos overworld listo
    # para que suene al volver al mundo
    if log[0] == "el enemigo ha sido derrotado!" and len(log) == 1:
        audio.playVictoryTheme(audio.OVERWORLD)

    def renderLoop():
        _drawCombatScene(enemy, message)
    gamestate.menuRenderLoop = renderLoop
    gamestate.buttons.clear()

    def button0func():
        if log[0] == "el enemigo ha sido derrotado!" and len(log) == 1:
            # el tema de victoria ya esta sonando. al salir arrancamos
            # la bgm del mundo (overworld) para que siga sonando
            audio.ensureWorldBgm()
            def exit():
                # el enemigo desaparece del mundo
                if enemy in gamestate.worldObjectList:
                    gamestate.worldObjectList.remove(enemy)
                gamestate.gameloop = "world"
            transition.start(exit, duration=2500)
            return
        elif log[0] == "el jugador ha perdido!!":
            # silencia la musica de combate y carga pantalla de game over
            import pygame as _pg
            _pg.mixer.music.stop()
            def toGameOver():
                loadGameOverMenu()
            transition.start(toGameOver, duration=1800)
            return
        if len(log) == 1:
            LoadTurnMenu(enemy)
        else:
            LoadLogMenu(enemy, log[1:])

    gamestate.buttons.append(Button(
        button0func, "siguiente", (255, 255, 255), (32, 32, 32), 0
    ))
    gamestate.buttons.append(Button(
        lambda: None, "", (255, 255, 255), (0, 0, 0), 1
    ))
    gamestate.buttons.append(Button(
        lambda: None, "", (255, 255, 255), (0, 0, 0), 2
    ))

    def button3func():
        # vuelve la musica del mundo ya, asi suena durante la transicion
        audio.ensureWorldBgm()
        def exit():
            gamestate.gameloop = "world"
        transition.start(exit, duration=2500)
    button3 = Button(
        button3func,
        "salir",
        (255, 255, 255),
        (32, 32, 32),
        3
    )
    gamestate.buttons.append(button3)
