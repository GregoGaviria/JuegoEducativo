import pygame


def _loadFrames(sheetPath, size, flip):
    sheet = pygame.image.load(sheetPath).convert_alpha()
    frameSize = sheet.get_height()
    count = sheet.get_width() // frameSize
    frames = []
    for i in range(count):
        sub = pygame.Surface((frameSize, frameSize), pygame.SRCALPHA)
        sub.blit(sheet, (0, 0), (i*frameSize, 0, frameSize, frameSize))
        scaled = pygame.transform.scale(sub, (size, size))
        if flip:
            scaled = pygame.transform.flip(scaled, True, False)
        frames.append(scaled)
    return frames


class CombatSprite():
    # flip=True invierte horizontalmente (ej: enemigo mirando al jugador)
    def __init__(self, idleSheet, attackSheet, size=320, flip=False):
        self.idleFrames = _loadFrames(idleSheet, size, flip)
        self.attackFrames = _loadFrames(attackSheet, size, flip)
        self.attacking = False
        self.attackStart = 0
        # 90ms por frame de ataque (~11 fps) para que se note el golpe
        self.attackFrameMs = 90
        self.idleFrameMs = 150

    def startAttack(self):
        self.attacking = True
        self.attackStart = pygame.time.get_ticks()

    def isAttacking(self):
        if not self.attacking:
            return False
        elapsed = pygame.time.get_ticks() - self.attackStart
        if elapsed >= self.attackFrameMs * len(self.attackFrames):
            self.attacking = False
            return False
        return True

    def draw(self, surface, x, y):
        now = pygame.time.get_ticks()
        if self.isAttacking():
            elapsed = now - self.attackStart
            idx = min(
                elapsed // self.attackFrameMs,
                len(self.attackFrames) - 1
            )
            surface.blit(self.attackFrames[idx], (x, y))
        else:
            idx = (now // self.idleFrameMs) % len(self.idleFrames)
            surface.blit(self.idleFrames[idx], (x, y))


# mapa de enemigo -> sheets
ENEMY_SHEETS = {
    "crasheador": (
        "assets/enemy-warrior_sheet.png",
        "assets/enemy-warrior_attack_sheet.png",
    ),
    "Gwifi": (
        "assets/enemy-archer_sheet.png",
        "assets/enemy-archer_attack_sheet.png",
    ),
    "pulgita": (
        "assets/enemy-pawn_sheet.png",
        "assets/enemy-pawn_attack_sheet.png",
    ),
    "Vibecoded Slop": (
        "assets/boss_sheet.png",
        "assets/boss_attack_sheet.png",
    ),
}


def forEnemy(enemy, size=320):
    idle, atk = ENEMY_SHEETS[enemy.combat.name]
    return CombatSprite(idle, atk, size=size, flip=True)


def forPlayer(size=320):
    return CombatSprite(
        "assets/player_sheet.png",
        "assets/player_attack_sheet.png",
        size=size,
        flip=False,
    )
