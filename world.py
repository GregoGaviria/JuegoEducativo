import config
import pygame
import gamestate
import globVariables
import worldObjects
import pygame.locals


def worldGameLoop():
    globVariables.DISPLAYSURF.fill((255, 255, 255))

    pygame.draw.rect(
        globVariables.DISPLAYSURF,
        (240, 20, 80),
        pygame.Rect(gamestate.posX, gamestate.posY, 60, 60)
    )

    # pygame.draw.rect(
    #     globVariables.DISPLAYSURF,
    #     (0, 0, 0),
    #     pygame.Rect(config.WIN_WIDTH/2-30, config.WIN_HEIGHT/2-30, 60, 60)
    # )
    libro = worldObjects.WorldObject(
        config.WIN_WIDTH/2-30, config.WIN_HEIGHT/2-30, "assets/placeholder-libro.jpg")
    libro.draw()

    pressedKeys = pygame.key.get_pressed()
    if pressedKeys[pygame.K_s]:
        gamestate.posY = gamestate.posY+3
    if pressedKeys[pygame.K_w]:
        gamestate.posY = gamestate.posY-3
    if pressedKeys[pygame.K_a]:
        gamestate.posX = gamestate.posX-3
    if pressedKeys[pygame.K_d]:
        gamestate.posX = gamestate.posX+3

    # event loop:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_i:
                    # if dentro de rango de libro
                    pass
                case pygame.K_q:
                    gamestate.gameloop = "menu"
        if event.type == pygame.constants.QUIT:
            gamestate.exitflag = True
