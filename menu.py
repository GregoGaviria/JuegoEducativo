import pygame
import gamestate
import audio
import transition


def _pressButton(idx):
    btn = gamestate.buttons[idx]
    # no reproducir SFX ni disparar funcion en slots vacios
    if btn.texto == "":
        return
    audio.playSelect()
    btn.function()


def menuGameLoop():
    gamestate.menuRenderLoop()
    for button in gamestate.buttons:
        button.render()
    for event in pygame.event.get():
        if event.type == pygame.constants.QUIT:
            gamestate.exitflag = True
            continue
        # durante la transicion se ignoran las teclas
        if transition.isActive():
            continue
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_u:
                    _pressButton(0)
                case pygame.K_i:
                    _pressButton(1)
                case pygame.K_o:
                    _pressButton(2)
                case pygame.K_p:
                    _pressButton(3)
