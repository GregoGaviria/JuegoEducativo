import pygame
import gamestate
import world
import menu
import pygame.locals
import globVariables
pygame.init()
pygame.font.init()
gamestate.init()
globVariables.init()
FPS = pygame.time.Clock()

pygame.display.set_caption("juego")

globVariables.DISPLAYSURF
posX, posY = 0, 0
while gamestate.exitflag == False:

    match gamestate.gameloop:
        case "menu":
            menu.menuWorldLoop()
        case "world":
            world.worldGameLoop()

    pygame.display.update()
    FPS.tick(60)

pygame.quit()
