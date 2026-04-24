import pygame
# pre-init del mixer ANTES de pygame.init() para bajar la latencia de
# los SFX (buffer de 256 samples ~5ms vs ~45ms del default de 2048).
# sin esto el sonido de espada arranca notablemente despues del golpe.
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=256)
import gamestate
import world
import menu
import pygame.locals
import globVariables
import menuEntries
import audio
import transition
import particles
pygame.init()
pygame.font.init()
pygame.mixer.init()
globVariables.init()
audio.init()
particles.init()
# menuEntries.init()
gamestate.init()
menuEntries.loadMainMenu()

# arranca con la cancion de zelda; mas adelante se reemplaza por overworld
audio.playBgm(audio.ZELDA)

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

    transition.update()
    audio.update()
    pygame.display.update()
    FPS.tick(60)

pygame.quit()
