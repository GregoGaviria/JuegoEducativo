import menuEntries
# import config
import pygame
import gamestate
import globVariables
import transition
import particles
# import worldObjects
import pygame.locals


def tryMovePlayer(dx, dy):
    playerRect = gamestate.player.worldObject.rect
    # intentamos mover en x e y por separado para que deslice sobre paredes
    playerRect.move_ip(dx, 0)
    if collidesWithWall(playerRect):
        playerRect.move_ip(-dx, 0)
    playerRect.move_ip(0, dy)
    if collidesWithWall(playerRect):
        playerRect.move_ip(0, -dy)


def collidesWithWall(rect):
    for obj in gamestate.worldObjectList:
        wo = obj.worldObject if hasattr(obj, "worldObject") else obj
        if wo.solid and wo.rect.colliderect(rect):
            return True
    return False


def worldGameLoop():
    # globVariables.DISPLAYSURF.fill((255, 255, 255))
    globVariables.DISPLAYSURF.blit(gamestate.worldBackground, (0, 0))

    gamestate.player.draw()

    for i in gamestate.worldObjectList:
        i.draw()

    # particulas ambientales flotando sobre el mundo
    particles.updateAmbient()
    particles.drawAmbient()

    # durante la transicion no se mueve ni se procesan teclas
    if transition.isActive():
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                gamestate.exitflag = True
        return

    pressedKeys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if pressedKeys[pygame.K_s]:
        dy += 3
    if pressedKeys[pygame.K_w]:
        dy -= 3
    if pressedKeys[pygame.K_a]:
        dx -= 3
    if pressedKeys[pygame.K_d]:
        dx += 3
    tryMovePlayer(dx, dy)

    # event loop:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_i:
                    # una vez que una interaccion dispara transicion
                    # (portal o combate), paramos para evitar que un
                    # enemigo cercano tambien dispare musica de combate
                    for i in gamestate.worldObjectList:
                        i.playerwithinrange()
                        if transition.isActive():
                            break
                case pygame.K_q:
                    menuEntries.loadMainMenu()
                    gamestate.gameloop = "menu"
        if event.type == pygame.constants.QUIT:
            gamestate.exitflag = True
