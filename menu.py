import pygame
import gamestate



def menuGameLoop():
    gamestate.menuRenderLoop()
    for button in gamestate.buttons:
        button.render()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_u:
                    gamestate.buttons[0].function()
                case pygame.K_i:
                    gamestate.buttons[1].function()
                case pygame.K_o:
                    gamestate.buttons[2].function()
                case pygame.K_p:
                    gamestate.buttons[3].function()
        if event.type == pygame.constants.QUIT:
            gamestate.exitflag = True
