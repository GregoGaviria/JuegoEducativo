import pygame
import globVariables


class WorldObject():
    def __init__(self, x, y, spritePath):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(spritePath)
        self.rect = self.sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):

        globVariables.DISPLAYSURF.blit(self.sprite, self.rect)
