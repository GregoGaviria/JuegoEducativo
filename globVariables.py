import pygame
import config


def init():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode(
        (config.WIN_HEIGHT, config.WIN_WIDTH)
    )
    global bg
    bg = pygame.image.load("assets/background-placeholder.jpg")
    global font
    font = pygame.font.SysFont("Noto Sans", 14)
