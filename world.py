import menuEntries
# import config
import pygame
import gamestate
import globVariables
# import worldObjects
import pygame.locals


def worldGameLoop():
    globVariables.DISPLAYSURF.fill((255, 255, 255))

    gamestate.player.draw()

    # libro = worldObjects.WorldObject(
    #     config.WIN_WIDTH/2-30, config.WIN_HEIGHT/2-30, "assets/placeholder-libro.jpg"
    # )
    # libro.draw()

    for i in gamestate.worldObjectList:
        i.draw()

    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[pygame.K_s]:
        gamestate.player.worldObject.rect.move_ip(0, 3)
    if pressedKeys[pygame.K_w]:
        gamestate.player.worldObject.rect.move_ip(0, -3)
    if pressedKeys[pygame.K_a]:
        gamestate.player.worldObject.rect.move_ip(-3, 0)
    if pressedKeys[pygame.K_d]:
        gamestate.player.worldObject.rect.move_ip(3, 0)

    # event loop:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_i:
                    # if gamestate.worldObjectList[0].playerwithinrange():
                    #     print("bastos")
                    #     menuEntries.loadBookMenu()
                    #     gamestate.gameloop = "menu"
                    for i in  gamestate.worldObjectList:
                        i.playerwithinrange()
                case pygame.K_q:
                    menuEntries.loadMainMenu()
                    gamestate.gameloop = "menu"
        if event.type == pygame.constants.QUIT:
            gamestate.exitflag = True
