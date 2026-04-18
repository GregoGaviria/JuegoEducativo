import random
import config
import math


class CombatUnit():
    def __init__(
        self,
        baseHP,
        baseAttack,
        baseDefense,
        baseSpatk,
        baseSpdef,
        baseSpeed,
        move0,
        move1,
        move2,
        weaknesses,
        types
    ):
        self.MAXHP = baseHP
        self.hp = self.MAXHP
        self.ATTACK = baseAttack
        self.DEFENSE = baseDefense
        self.SPATK = baseSpatk
        self.SPDEF = baseSpdef
        self.SPEED = baseSpeed

        self.move0 = move0
        self.move1 = move1
        self.move2 = move2

        self.attackBoost = 0
        self.defenseBoost = 0
        self.spatkBoost = 0
        self.spdefBoost = 0
        self.speedBoost = 0
        self.evasion = 0
        self.accuracy = 0


class Move():
    def __init__(
        self,
        moveName,
        desc,
        moveBP,
        moveACC,
        moveType,
        effect,
        special
    ):
        self.name = moveName
        self.bp = moveBP
        self.acc = moveACC
        self.type = moveType
        self.effect = effect
        self.desc = desc
        self.special = special

    def use(self, target, user):
        def applyBoost(stat, boost, denominator):
            multiplier = 1
            if boost > 6:
                boost = 6
                multiplier = ((denominator+boost)/denominator)
            elif boost < -6:
                boost = -6
                multiplier = (denominator/(denominator-boost))
            elif boost < 0:
                multiplier = (denominator/(denominator-boost))
            elif boost > 0:
                multiplier = ((denominator+boost)/denominator)
            return multiplier*stat
        battleLog = []

        accStat = applyBoost(self.acc, user.accuracy-target.evasion, 3)
        if accStat < random.randint(0, 100):
            battleLog.append("el movimiento fallo!")
            return battleLog

        attackingStat = 0
        defendingStat = 0
        if self.special:
            attackingStat = applyBoost(user.SPATK, user.spatkBoost, 2)
            defendingStat = applyBoost(user.SPDEF, user.spdefBoost, 2)
        else:
            attackingStat = applyBoost(user.ATTACK, user.attackBoost, 2)
            defendingStat = applyBoost(user.DEFENSE, user.defenseBoost, 2)

        damage = self.bp*(attackingStat/defendingStat)
        damage = damage*(random.randint(85, 100)/100)
        if 100-config.CRIT_CHANCE < random.randint(0, 100):
            battleLog.append("golpe critico!")
            damage = damage*1.5

        damage = math.ceil(damage)
        target.hp = target.hp - damage

        battleLog = self.effect(target, user, battleLog)
        return battleLog
