import combat


def getUnitTest():
    return combat.Move(
        "Unit Test",
        "prueba de una unidad aislada, sin efecto adicional",
        130,
        65,
        "unit",
        lambda a, b, c: None,
        False
    )


def reduceEvasion(target, user, battleLog):
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
        reduceEvasion,
        False
    )


def reduce2selfSpatk(target, user, battleLog):
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
        reduce2selfSpatk,
        True
    )
