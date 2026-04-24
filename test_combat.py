import unittest
from unittest.mock import patch

import combat
import movelist


# helper para crear CombatUnits con defaults razonables
def makeUnit(
    name="test",
    hp=500,
    attack=100,
    defense=100,
    spatk=100,
    spdef=100,
    speed=100,
    weaknesses=None,
    resists=None,
    immunities=None,
    types=None
):
    return combat.CombatUnit(
        name=name,
        baseHP=hp,
        baseAttack=attack,
        baseDefense=defense,
        baseSpatk=spatk,
        baseSpdef=spdef,
        baseSpeed=speed,
        move0=movelist.getUnitTest(),
        move1=movelist.getIntegrationTest(),
        move2=movelist.getSystemTest(),
        weaknesses=weaknesses if weaknesses is not None else [],
        resists=resists if resists is not None else [],
        immunities=immunities if immunities is not None else [],
        types=types if types is not None else []
    )


def makeMove(name="test", bp=50, acc=100, tipo="normal", special=False,
             effect=None):
    if effect is None:
        effect = lambda target, user, log: log
    return combat.Move(name, "", bp, acc, tipo, effect, special)


# fakeRandint controla las 3 llamadas de Move.use:
#   accuracy check (0, 100)      -> 0 pasa siempre
#   variacion de daño (85, 100)  -> 100 = daño completo
#   critico (0, 100)             -> 0 = nunca critico
def fakeRandint(a, b):
    if (a, b) == (85, 100):
        return 100
    return 0


class TestCombatUnit(unittest.TestCase):
    def setUp(self):
        self.unit = makeUnit(
            hp=200,
            attack=80,
            defense=70,
            spatk=90,
            spdef=60,
            speed=110,
            types=["unit"],
            weaknesses=["bug"],
            resists=["network"],
            immunities=["irritating"]
        )

    def testHpArrancaEnMaximo(self):
        self.assertEqual(self.unit.hp, 200)
        self.assertEqual(self.unit.MAXHP, 200)

    def testStatsAsignadas(self):
        self.assertEqual(self.unit.ATTACK, 80)
        self.assertEqual(self.unit.DEFENSE, 70)
        self.assertEqual(self.unit.SPATK, 90)
        self.assertEqual(self.unit.SPDEF, 60)
        self.assertEqual(self.unit.SPEED, 110)

    def testBoostsArrancanEnCero(self):
        self.assertEqual(self.unit.attackBoost, 0)
        self.assertEqual(self.unit.defenseBoost, 0)
        self.assertEqual(self.unit.spatkBoost, 0)
        self.assertEqual(self.unit.spdefBoost, 0)
        self.assertEqual(self.unit.speedBoost, 0)
        self.assertEqual(self.unit.evasion, 0)
        self.assertEqual(self.unit.accuracy, 0)

    def testTiposYDebilidades(self):
        self.assertIn("unit", self.unit.TYPES)
        self.assertIn("bug", self.unit.WEAKNESSES)
        self.assertIn("network", self.unit.RESISTS)
        self.assertIn("irritating", self.unit.IMMUNITIES)


class TestMoveCreacion(unittest.TestCase):
    def testCamposAsignados(self):
        move = combat.Move(
            "prueba", "una descripcion", 80, 95, "unit",
            lambda t, u, log: log, True
        )
        self.assertEqual(move.name, "prueba")
        self.assertEqual(move.desc, "una descripcion")
        self.assertEqual(move.bp, 80)
        self.assertEqual(move.acc, 95)
        self.assertEqual(move.type, "unit")
        self.assertTrue(move.special)


class TestMoveUse(unittest.TestCase):
    def setUp(self):
        self.attacker = makeUnit(name="atacante")
        self.defender = makeUnit(name="defensor", hp=1000)

    def testDanioReduceHpDelObjetivo(self):
        move = makeMove(bp=50, acc=100, tipo="normal")
        hpInicial = self.defender.hp
        with patch("combat.random.randint", side_effect=fakeRandint):
            move.use(self.defender, self.attacker)
        self.assertLess(self.defender.hp, hpInicial)

    def testMovimientoFalla(self):
        move = makeMove(bp=50, acc=1, tipo="normal")
        hpInicial = self.defender.hp
        # accStat = 1, randint devuelve 100 -> 1 < 100 -> falla
        with patch("combat.random.randint", return_value=100):
            log = move.use(self.defender, self.attacker)
        self.assertEqual(self.defender.hp, hpInicial)
        self.assertIn("el movimiento fallo!", log)

    def testDebilidadDuplicaDanio(self):
        normal = makeUnit(name="normal", hp=1000)
        debil = makeUnit(name="debil", hp=1000, weaknesses=["normal"])
        move = makeMove(bp=50, acc=100, tipo="normal")

        with patch("combat.random.randint", side_effect=fakeRandint):
            move.use(normal, self.attacker)
        with patch("combat.random.randint", side_effect=fakeRandint):
            log = move.use(debil, self.attacker)

        danioNormal = 1000 - normal.hp
        danioDebil = 1000 - debil.hp
        self.assertGreater(danioDebil, danioNormal)
        self.assertIn("el movimiento es super effectivo!", log)

    def testResistenciaReduceDanio(self):
        normal = makeUnit(name="normal", hp=1000)
        resistente = makeUnit(name="resistente", hp=1000, resists=["normal"])
        move = makeMove(bp=50, acc=100, tipo="normal")

        with patch("combat.random.randint", side_effect=fakeRandint):
            move.use(normal, self.attacker)
        with patch("combat.random.randint", side_effect=fakeRandint):
            log = move.use(resistente, self.attacker)

        danioNormal = 1000 - normal.hp
        danioResistente = 1000 - resistente.hp
        self.assertLess(danioResistente, danioNormal)
        self.assertIn("el movimiento no es muy efectivo", log)

    def testStabAumentaDanio(self):
        atkSinStab = makeUnit(name="sinstab", types=[])
        atkConStab = makeUnit(name="constab", types=["normal"])
        d1 = makeUnit(name="d1", hp=1000)
        d2 = makeUnit(name="d2", hp=1000)
        move = makeMove(bp=50, acc=100, tipo="normal")

        with patch("combat.random.randint", side_effect=fakeRandint):
            move.use(d1, atkSinStab)
        with patch("combat.random.randint", side_effect=fakeRandint):
            move.use(d2, atkConStab)

        self.assertGreater(1000 - d2.hp, 1000 - d1.hp)

    def testCriticoAumentaDanio(self):
        d1 = makeUnit(name="d1", hp=1000)
        d2 = makeUnit(name="d2", hp=1000)
        move = makeMove(bp=50, acc=100, tipo="normal")
        # sin critico: [acc=0, var=100, crit=0]
        with patch("combat.random.randint", side_effect=[0, 100, 0]):
            move.use(d1, self.attacker)
        # con critico: [acc=0, var=100, crit=100]
        with patch("combat.random.randint", side_effect=[0, 100, 100]):
            log = move.use(d2, self.attacker)
        self.assertGreater(1000 - d2.hp, 1000 - d1.hp)
        self.assertIn("golpe critico!", log)

    def testEfectoPersonalizadoSeEjecuta(self):
        marcador = []

        def efecto(target, user, log):
            marcador.append("ejecutado")
            log.append("efecto custom")
            return log

        move = combat.Move("x", "", 50, 100, "normal", efecto, False)
        with patch("combat.random.randint", side_effect=fakeRandint):
            log = move.use(self.defender, self.attacker)
        self.assertIn("ejecutado", marcador)
        self.assertIn("efecto custom", log)


class TestInitTurn(unittest.TestCase):
    def testJugadorMasRapidoAtacaPrimero(self):
        jugador = makeUnit(name="jugador", speed=200)
        enemigo = makeUnit(name="enemigo", speed=50)
        move = makeMove(bp=1, acc=100, tipo="normal")
        with patch("combat.random.choice", return_value=move):
            with patch("combat.random.randint", side_effect=fakeRandint):
                log = combat.initTurn(move, jugador, enemigo)
        # la primera linea del log nombra al primer atacante
        self.assertIn("jugador", log[0])

    def testEnemigoMasRapidoAtacaPrimero(self):
        jugador = makeUnit(name="jugador", speed=10)
        enemigo = makeUnit(name="enemigo", speed=200)
        move = makeMove(bp=1, acc=100, tipo="normal")
        with patch("combat.random.choice", return_value=move):
            with patch("combat.random.randint", side_effect=fakeRandint):
                log = combat.initTurn(move, jugador, enemigo)
        self.assertIn("enemigo", log[0])

    def testKoDelEnemigoSeMencionaEnLog(self):
        jugador = makeUnit(name="jugador", attack=9999, speed=200)
        enemigo = makeUnit(name="enemigo", hp=1, defense=1, speed=10)
        move = makeMove(bp=200, acc=100, tipo="normal")
        with patch("combat.random.choice", return_value=move):
            with patch("combat.random.randint", side_effect=fakeRandint):
                log = combat.initTurn(move, jugador, enemigo)
        self.assertTrue(
            any("enemigo ha sido derrotado" in linea for linea in log)
        )


# estos tests documentan bugs que existian antes y que ya fueron
# arreglados. se quedan como evidencia de regresion: si alguien
# rompe estas invariantes de nuevo, el test salta.
class TestBugsArreglados(unittest.TestCase):
    # antes: combat.py dividia el daño entre 2 en inmunidades
    # en vez de dejarlo en 0. ahora el daño queda en 0.
    def testInmunidadAnulaDanio(self):
        inmune = makeUnit(name="inmune", hp=1000, immunities=["normal"])
        atacante = makeUnit(name="atk")
        move = makeMove(bp=50, acc=100, tipo="normal")
        with patch("combat.random.randint", side_effect=fakeRandint):
            move.use(inmune, atacante)
        self.assertEqual(inmune.hp, 1000)

    # antes: movelist.py usaba random.choice(target, user) lo que
    # crasheaba el combate (choice espera un iterable, no dos args).
    def testRevolverDatosNoCrashea(self):
        target = makeUnit(name="t")
        user = makeUnit(name="u")
        movelist.getRevolverDatos().effect(target, user, [])

    # antes: __scrambleStats no hacia "return battleLog", entonces
    # Move.use terminaba devolviendo None y combat.initTurn crasheaba
    # con TypeError al concatenar list + None.
    def testRevolverDatosRetornaBattleLog(self):
        target = makeUnit(name="t")
        user = makeUnit(name="u")
        result = movelist.getRevolverDatos().effect(target, user, ["hola"])
        self.assertIsInstance(result, list)
        self.assertIn("hola", result)

    # antes: __reduceAccuracy sumaba +1 en vez de restar, o sea
    # "irritar" aumentaba la precision en lugar de reducirla.
    def testIrritarReducePrecision(self):
        target = makeUnit(name="t")
        user = makeUnit(name="u")
        accInicial = target.accuracy
        movelist.getIrritar().effect(target, user, [])
        self.assertLess(target.accuracy, accInicial)


if __name__ == "__main__":
    unittest.main()
