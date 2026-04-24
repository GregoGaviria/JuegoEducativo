import pygame
import config


def init():
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode(
        (config.WIN_HEIGHT, config.WIN_WIDTH)
    )
    global font
    font = pygame.font.SysFont("Noto Sans", 14)
    global buttonKeyFont
    buttonKeyFont = pygame.font.SysFont("Noto Sans", 20, bold=True)
    # fuentes del libro
    global docTitleFont
    docTitleFont = pygame.font.SysFont("Noto Sans", 28, bold=True)
    global docBodyFont
    docBodyFont = pygame.font.SysFont("Noto Sans", 18)
    global docPageFont
    docPageFont = pygame.font.SysFont("Noto Sans", 14, italic=True)
    global worldBackground
    worldBackground = pygame.transform.scale(
        pygame.image.load("assets/world-bg.png"),
        (config.WIN_WIDTH, config.WIN_HEIGHT)
    )
    # mismo fondo para los menus (consistencia visual)
    global menuBackground
    menuBackground = worldBackground
    # fondo dramatico solo para la batalla contra el jefe
    global bossBattleBackground
    bossBattleBackground = pygame.transform.scale(
        pygame.image.load("assets/boss-bg.png"),
        (config.WIN_WIDTH, config.WIN_HEIGHT)
    )
