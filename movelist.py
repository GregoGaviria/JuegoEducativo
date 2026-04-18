import combat


def getUnitTest():
    return combat.Move(
        "Unit Test",
        "prueba de una unidad aislada, sin efecto adicional",
        130,
        65,
        "unit",
        lambda a, b, c: c,
        False
    )


def __reduceEvasion(target, user, battleLog):
    target.evasion = target.evasion-1
    battleLog.append("se redujo la evasión")
    return battleLog


def getIntegrationTest():
    return combat.Move(
        "Integration test",
        "prueba para multiples componentes, reduce evasión de enemigo",
        55,
        85,
        "integration",
        __reduceEvasion,
        False
    )


def __reduce2selfSpatk(target, user, battleLog):
    user.spatkBoost = user.spatkBoost-2
    battleLog.append("se redujo el ataque especial")
    return battleLog


def getSystemTest():
    return combat.Move(
        "system test",
        "prueba de sistema completo, reduce tu propio ataque",
        190,
        85,
        "system",
        __reduce2selfSpatk,
        True
    )


def getCrash():
    return combat.Move(
        "crash",
        "bota el sistema",
        140,
        100,
        "irritating",
        __reduce2selfSpatk,
        True
    )
