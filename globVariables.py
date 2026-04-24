import pygame
import config


def init():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode(
        (config.WIN_HEIGHT, config.WIN_WIDTH)
    )
    global font
    font = pygame.font.SysFont("Noto Sans", 14)
    global worldBackground
    worldBackground = pygame.transform.scale(
        pygame.image.load("assets/bacground-world-placeholder.jpg"),
        (config.WIN_WIDTH, config.WIN_HEIGHT)
    )
