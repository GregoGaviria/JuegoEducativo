import combat
import random


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
    battleLog.append("se redujo la evasión de "+target.name)
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
    battleLog.append("se redujo el ataque especial de "+user.name)
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
        130,
        100,
        "normal",
        __reduce2selfSpatk,
        False
    )


def getBluescreen():
    return combat.Move(
        "bluescreen",
        "",
        65,
        90,
        "irritating",
        lambda a, b, c: c,
        True
    )


def __reduceAccuracy(target, user, battleLog):
    target.accuracy = target.accuracy+1
    battleLog.append("se redujo la precision de "+target.name)
    return battleLog


def getIrritar():
    return combat.Move(
        "irritar",
        "",
        1,
        100,
        "irritating",
        __reduceAccuracy,
        False
    )


def __reduce2Speed(target, user, battleLog):
    target.speedBoost = target.speedBoost - 2
    battleLog.append("se redujo la velocidad de "+target.name)
    return battleLog


def getVelocidadBaja():
    return combat.Move(
        "velocidad baja",
        "",
        10,
        100,
        "network",
        __reduce2Speed,
        True
    )


def getOutage():
    return combat.Move(
        "outage",
        "",
        80,
        90,
        "network",
        lambda a, b, c: c,
        True
    )


def __reduceAttack(target, user, battleLog):
    target.attackBoost = target.attackBoost - 1
    battleLog.append("se redujo el ataque de "+target.name)
    return battleLog


def getIntermitencia():
    return combat.Move(
        "Intermitencia",
        "",
        20,
        80,
        "network",
        __reduceAttack,
        True
    )


def __scrambleStats(target, user, battleLog):
    battleLog.append("se revuelven las estadisticas")
    kaisuu = random.randint(1, 2)
    for i in range(kaisuu):
        tget = random.choice(target, user)
        teido = random.randint(1, 2)
        match random.randint(1, 2):
            case 1:
                match random.randint(1, 7):
                    case 1:
                        tget.attackBoost = tget.attackBoost - teido
                        battleLog.append(
                            'se redujo el ataque de '+tget.name
                        )
                    case 2:
                        tget.defenseBoost = tget.defenseBoost - teido
                        battleLog.append(
                            'se redujo la defensa de '+tget.name
                        )
                    case 3:
                        tget.spatkBoost = tget.spatkBoost - teido
                        battleLog.append(
                            'se redujo el ataque especial de '+tget.name
                        )
                    case 4:
                        tget.spdefBoost = tget.spdefBoost - teido
                        battleLog.append(
                            'se redujo la defensa especial de '+tget.name
                        )
                    case 5:
                        tget.speedBoost = tget.speedBoost - teido
                        battleLog.append(
                            'se redujo la velocidad de '+tget.name
                        )
                    case 6:
                        tget.evasion = tget.evasion - teido
                        battleLog.append(
                            'se redujo la evasion de '+tget.name
                        )
                    case 7:
                        tget.accuracy = tget.accuracy - teido
                        battleLog.append(
                            'se redujo la precision de '+tget.name
                        )

            case 2:
                match random.randint(1, 7):
                    case 1:
                        tget.attackBoost = tget.attackBoost + teido
                        battleLog.append(
                            'se aumento el ataque de '+tget.name
                        )
                    case 2:
                        tget.defenseBoost = tget.defenseBoost + teido
                        battleLog.append(
                            'se aumento la defensa de '+tget.name
                        )
                    case 3:
                        tget.spatkBoost = tget.spatkBoost + teido
                        battleLog.append(
                            'se aumento el ataque especial de '+tget.name
                        )
                    case 4:
                        tget.spdefBoost = tget.spdefBoost + teido
                        battleLog.append(
                            'se aumento la defensa especial de '+tget.name
                        )
                    case 5:
                        tget.speedBoost = tget.speedBoost + teido
                        battleLog.append(
                            'se aumento la velocidad de '+tget.name
                        )
                    case 6:
                        tget.evasion = tget.evasion + teido
                        battleLog.append(
                            'se aumento la evasion de '+tget.name
                        )
                    case 7:
                        tget.accuracy = tget.accuracy + teido
                        battleLog.append(
                            'se aumento la precision de '+tget.name
                        )


def getRevolverDatos():
    return combat.Move(
        "revolver datos",
        "",
        60,
        75,
        "bug",
        __scrambleStats,
        False
    )


def getRomperInterfazVisual():
    return combat.Move(
        "romper interfaz grafica",
        "",
        90,
        80,
        "bug",
        __reduceAccuracy,
        True
    )
