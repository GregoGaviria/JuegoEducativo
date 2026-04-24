import pygame

# paths
ZELDA = "assets/bgm.mp3"
OVERWORLD = "assets/overworld.mp3"
MAIN_BATTLE = "assets/main_battle.mp3"
FINAL_BATTLE = "assets/final_battle.mp3"
VICTORY_THEME = "assets/win_battle.mp3"

# estado interno
_currentBgm = None
_worldBgm = ZELDA  # al inicio, zelda es la bgm del mundo
_sfxChannel = None

# sounds
SELECT = None
SLASH = None
SUPER = None


def init():
    global SELECT, SLASH, SUPER, _sfxChannel
    SELECT = pygame.mixer.Sound("assets/sfx_select.mp3")
    SLASH = pygame.mixer.Sound("assets/sfx_slash.mp3")
    SUPER = pygame.mixer.Sound("assets/sfx_super.mp3")
    SELECT.set_volume(0.6)
    SLASH.set_volume(0.85)
    SUPER.set_volume(0.8)
    _sfxChannel = pygame.mixer.Channel(2)
    # "calentar" los SFX: primera reproduccion en pygame suele tener
    # un retardo extra por la decodificacion JIT del mp3. los tocamos
    # una vez a volumen 0 para que la segunda sea instantanea
    _warmCh = pygame.mixer.Channel(7)
    oldVols = (SELECT.get_volume(), SLASH.get_volume(), SUPER.get_volume())
    for s in (SELECT, SLASH, SUPER):
        s.set_volume(0)
        _warmCh.play(s)
        _warmCh.stop()
    SELECT.set_volume(oldVols[0])
    SLASH.set_volume(oldVols[1])
    SUPER.set_volume(oldVols[2])


def playBgm(path):
    global _currentBgm, _nextBgmAfterJingle
    # si ya estamos sonando esto, no hacer nada
    if _currentBgm == path and pygame.mixer.music.get_busy():
        return
    _currentBgm = path
    _nextBgmAfterJingle = None
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print("no se pudo cargar la musica:", path, e)


def setWorldBgm(path):
    global _worldBgm
    _worldBgm = path


def ensureWorldBgm():
    playBgm(_worldBgm)


def startBattleBgm():
    playBgm(MAIN_BATTLE)


# al mostrar la linea final de victoria arrancamos el tema de victoria
# como bgm (loop) y tambien configuramos la bgm del mundo a aplicar
# cuando el jugador salga del sistema de combate (ensureWorldBgm)
def playVictoryTheme(newWorldBgm=None):
    if newWorldBgm is not None:
        setWorldBgm(newWorldBgm)
    playBgm(VICTORY_THEME)


# placeholder para compatibilidad con main loop existente
def update():
    pass


def playSelect():
    _sfxChannel.play(SELECT)


def playSlash():
    _sfxChannel.play(SLASH)


def playSuperEffective():
    # se mezcla con slash en su propio canal
    pygame.mixer.Channel(3).play(SUPER)
