import pygame
import config
import globVariables


class Document():
    def __init__(self, textMatrix, textColor):
        self.currentPage = 0
        self.textMatrix = textMatrix
        self.textColor = textColor
        # panel semi transparente tipo pergamino
        panelWidth = config.WIN_WIDTH - 2*config.DOC_MARGIN_X
        panelHeight = (
            config.WIN_HEIGHT - config.DOC_MARGIN_TOP - config.DOC_MARGIN_BOTTOM
        )
        self.panel = pygame.Surface(
            (panelWidth, panelHeight),
            pygame.SRCALPHA
        )
        self.panel.fill((245, 238, 214, 225))
        self.panelRect = self.panel.get_rect()
        self.panelRect.x = config.DOC_MARGIN_X
        self.panelRect.y = config.DOC_MARGIN_TOP
        # borde oscuro del panel
        self.panelBorder = pygame.Rect(
            self.panelRect.x,
            self.panelRect.y,
            panelWidth,
            panelHeight
        )
        self.loadPages()

    def loadPages(self):
        titleSurface = None
        bodySurfaces = []
        titleDone = False
        for line in self.textMatrix[self.currentPage]:
            if (not titleDone) and line.strip() != "":
                titleSurface = globVariables.docTitleFont.render(
                    line, True, self.textColor
                )
                titleDone = True
            else:
                bodySurfaces.append(
                    globVariables.docBodyFont.render(
                        line, True, self.textColor
                    )
                )
        self.titleSurface = titleSurface
        self.bodySurfaces = bodySurfaces
        self.pageIndicator = globVariables.docPageFont.render(
            "pagina " + str(self.currentPage+1) +
            " / " + str(len(self.textMatrix)),
            True,
            self.textColor
        )

    def render(self):
        globVariables.DISPLAYSURF.blit(globVariables.menuBackground, (0, 0))
        globVariables.DISPLAYSURF.blit(self.panel, self.panelRect)
        pygame.draw.rect(
            globVariables.DISPLAYSURF,
            (60, 40, 20),
            self.panelBorder,
            2
        )
        yCursor = self.panelRect.y + config.DOC_PADDING
        # titulo centrado
        if self.titleSurface is not None:
            titleX = (
                self.panelRect.x +
                (self.panelRect.width - self.titleSurface.get_width())/2
            )
            globVariables.DISPLAYSURF.blit(
                self.titleSurface,
                (titleX, yCursor)
            )
            # linea decorativa debajo del titulo
            underlineY = yCursor + self.titleSurface.get_height() + 4
            underlineWidth = min(
                self.titleSurface.get_width() + 40,
                self.panelRect.width - 2*config.DOC_PADDING
            )
            underlineX = (
                self.panelRect.x +
                (self.panelRect.width - underlineWidth)/2
            )
            pygame.draw.line(
                globVariables.DISPLAYSURF,
                (120, 80, 40),
                (underlineX, underlineY),
                (underlineX + underlineWidth, underlineY),
                1
            )
            yCursor += (
                self.titleSurface.get_height() + config.DOC_TITLE_GAP
            )
        # cuerpo
        bodyX = self.panelRect.x + config.DOC_PADDING
        for surface in self.bodySurfaces:
            globVariables.DISPLAYSURF.blit(surface, (bodyX, yCursor))
            yCursor += config.DOC_LINE_GAP
        # indicador de pagina en esquina inferior derecha del panel
        indicatorX = (
            self.panelRect.x + self.panelRect.width -
            self.pageIndicator.get_width() - config.DOC_PADDING
        )
        indicatorY = (
            self.panelRect.y + self.panelRect.height -
            self.pageIndicator.get_height() - 12
        )
        globVariables.DISPLAYSURF.blit(
            self.pageIndicator,
            (indicatorX, indicatorY)
        )

    def nextPage(self):
        max = len(self.textMatrix)-1
        if self.currentPage < max:
            self.currentPage += 1
        self.loadPages()

    def prevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
        self.loadPages()


def getLibro():
    return Document(
        [
            [
                "bienvenido al juego!",
                "",
                "aca aprenderas sobre pruebas de software",
                "mientras te enfrentas a bugs y fallos.",
                "",
                "controles en el mundo:",
                "  w a s d  para moverte",
                "  i  para interactuar con objetos",
                "  q  para volver al menu principal",
                "",
                "en los menus usa:",
                "  u i o p  para los 4 botones",
                "",
                "pasa de pagina para seguir leyendo.",
            ],
            [
                "como funciona el combate:",
                "",
                "cada enemigo representa un problema",
                "comun del software (un bug, una caida",
                "de red, un crasheo, etc).",
                "",
                "tus ataques son tipos de prueba:",
                "  unit test",
                "  integration test",
                "  system test",
                "",
                "elegi la prueba correcta para la",
                "situacion y vas a hacer mas daño.",
                "",
                "el que tiene mas velocidad ataca",
                "primero en el turno.",
            ],
            [
                "unit test (prueba unitaria):",
                "",
                "verifica una unidad aislada del codigo,",
                "como una funcion o un metodo pequeño,",
                "sin depender de otros modulos.",
                "",
                "sirve cuando queres confirmar que una",
                "pieza individual funciona bien antes",
                "de integrarla con el resto del sistema.",
                "",
                "en el juego es fuerte contra bugs",
                "pequeños y puntuales, como 'pulgita'.",
                "",
                "tip: mucho poder base pero poca",
                "precision, cuidado al fallar!",
            ],
            [
                "integration test (prueba de integracion):",
                "",
                "prueba como se comunican varios",
                "componentes o modulos entre si.",
                "",
                "sirve cuando dos piezas funcionan",
                "bien por separado pero al conectarlas",
                "aparecen fallos: apis que no responden,",
                "datos que pasan mal, conexiones que",
                "se caen a mitad de camino.",
                "",
                "en el juego es fuerte contra problemas",
                "de red como 'Gwifi'.",
                "",
                "efecto extra: reduce la evasion del",
                "enemigo, mas dificil que te esquive.",
            ],
            [
                "system test (prueba de sistema):",
                "",
                "valida el sistema completo funcionando",
                "como un todo, de punta a punta.",
                "",
                "sirve para comprobar que todos los",
                "modulos juntos cumplen los requisitos",
                "del proyecto y que el usuario final",
                "puede hacer lo que necesita.",
                "",
                "es la prueba mas poderosa del juego",
                "pero cada vez que la usas baja tu",
                "ataque especial (cuesta recursos!).",
                "",
                "fuerte contra fallos criticos e",
                "irritantes como 'crasheador'.",
            ],
            [
                "consejos finales:",
                "",
                "revisa el tipo del enemigo antes de",
                "elegir tu ataque. si el tipo de tu",
                "prueba es debil contra el enemigo",
                "el daño se duplica!",
                "",
                "si el enemigo resiste tu tipo el",
                "daño se reduce a la mitad.",
                "",
                "los golpes criticos suman un 50%",
                "extra de daño al azar.",
                "",
                "cada prueba tiene su momento, no",
                "existe una prueba perfecta para",
                "todo. aprende a combinarlas!",
                "",
                "suerte, y a testear!",
            ],
        ],
        (50, 30, 15),
    )
