import pygame
import gamestate
import menuEntries



def menuGameLoop():
    gamestate.currentMenu()
    for button in menuEntries.buttons:
        button.render()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_u:
                    menuEntries.buttons[0].function()
                case pygame.K_i:
                    menuEntries.buttons[1].function()
                case pygame.K_o:
                    menuEntries.buttons[2].function()
                case pygame.K_p:
                    menuEntries.buttons[3].function()
        if event.type == pygame.constants.QUIT:
            gamestate.exitflag = True
