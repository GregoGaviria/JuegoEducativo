import pygame
import config
import globVariables


def getDocTextX():
    return config.WIN_WIDTH/4


def getDocTextY(lineCount):
    return 10 + lineCount*config.TEXT_GAP


class Document():
    def __init__(self, textMatrix, textColor, bgImage):
        self.currentPage = 0
        self.textMatrix = textMatrix
        self.textColor = textColor
        self.loadPages()
        self.background = pygame.image.load(bgImage)

    def loadPages(self):
        fontLineList = []
        for i in self.textMatrix[self.currentPage]:
            fontLineList.append(globVariables.font.render(
                i,
                False,
                self.textColor
            ))
        self.textSurfaces = fontLineList

    def render(self):
        lineCount = 0
        for i in self.textSurfaces:
            globVariables.DISPLAYSURF.blit(
                i,
                (getDocTextX(), getDocTextY(lineCount))
            )
            lineCount += 1

    def nextPage(self):
        max = len(self.textMatrix)-1
        if self.currentPage < max:
            self.currentPage += 1
        self.loadPages()

    def prevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
        self.loadPages()
