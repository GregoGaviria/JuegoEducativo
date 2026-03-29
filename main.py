import pygame
import gamestate
import world
import menu
import pygame.locals
import globVariables
import menuEntries
pygame.init()
pygame.font.init()
globVariables.init()
menuEntries.init()
gamestate.init()
menuEntries.loadMainMenu()

FPS = pygame.time.Clock()

pygame.display.set_caption("juego")

globVariables.DISPLAYSURF
posX, posY = 0, 0
while gamestate.exitflag == False:

    match gamestate.gameloop:
        case "menu":
            menu.menuGameLoop()
        case "world":
            world.worldGameLoop()

    pygame.display.update()
    FPS.tick(60)

pygame.quit()
