import worldObjects


# cada isla es un dict con:
#   background: path al PNG de fondo
#   objects: lista de WorldObjects (enemigos, decoraciones, portales...)
#   defaultSpawn: (x, y) donde aparece el jugador la primera vez
def build():
    return [
        _buildIsland0(),
        _buildIsland1(),
        _buildIsland2(),
    ]


def _buildIsland0():
    objs = []
    # libro (solo en la primera isla)
    objs.append(worldObjects.getLibro())
    # casitas
    objs.append(worldObjects.getHouse(580, 150, variant=1))
    objs.append(worldObjects.getHouse(420, 620, variant=2))
    # ovejitas
    objs.append(worldObjects.getSheep(300, 540))
    objs.append(worldObjects.getSheep(560, 420))
    objs.append(worldObjects.getSheep(380, 700))
    # arboles en el perimetro
    for x, y in [(120, 160), (140, 700), (720, 220), (760, 680),
                 (220, 120), (680, 120), (660, 760)]:
        objs.append(worldObjects.getTree(x, y))
    # arbustos para texturizar
    for x, y in [(220, 420), (520, 300), (680, 540), (420, 420)]:
        objs.append(worldObjects.getBush(x, y))
    # 3 enemigos
    objs.append(worldObjects.getEnemyAt("crasheador", 360, 280))
    objs.append(worldObjects.getEnemyAt("conexion", 640, 480))
    objs.append(worldObjects.getEnemyAt("pulgita", 280, 620))
    # portal a la isla 1 (lado derecho)
    objs.append(worldObjects.Portal(
        x=770, y=430,
        targetIsland=1,
        targetSpawn=(140, 440),
        direction="right"
    ))
    return {
        "background": "assets/island0-bg.png",
        "objects": objs,
        "defaultSpawn": (440, 460),
    }


def _buildIsland1():
    objs = []
    # casitas (pueblito intermedio)
    objs.append(worldObjects.getHouse(280, 180, variant=3))
    objs.append(worldObjects.getHouse(500, 180, variant=1))
    objs.append(worldObjects.getHouse(380, 620, variant=2))
    # ovejitas
    objs.append(worldObjects.getSheep(200, 440))
    objs.append(worldObjects.getSheep(640, 440))
    # arboles
    for x, y in [(140, 200), (720, 180), (140, 640),
                 (720, 640), (400, 760)]:
        objs.append(worldObjects.getTree(x, y))
    # arbustos
    for x, y in [(260, 440), (560, 440), (400, 320),
                 (200, 680), (640, 680)]:
        objs.append(worldObjects.getBush(x, y))
    # 3 enemigos
    objs.append(worldObjects.getEnemyAt("conexion", 400, 240))
    objs.append(worldObjects.getEnemyAt("pulgita", 260, 540))
    objs.append(worldObjects.getEnemyAt("crasheador", 580, 540))
    # portal izquierdo: vuelve a isla 0
    objs.append(worldObjects.Portal(
        x=80, y=430,
        targetIsland=0,
        targetSpawn=(720, 440),
        direction="left"
    ))
    # portal derecho: a isla 2 (boss)
    objs.append(worldObjects.Portal(
        x=770, y=430,
        targetIsland=2,
        targetSpawn=(140, 440),
        direction="right"
    ))
    return {
        "background": "assets/island1-bg.png",
        "objects": objs,
        "defaultSpawn": (440, 460),
    }


def _buildIsland2():
    objs = []
    # la isla del boss: mas rocosa, menos casas
    objs.append(worldObjects.getHouse(160, 180, variant=3))
    # ovejitas (ultimos supervivientes...)
    objs.append(worldObjects.getSheep(220, 640))
    # arboles pocos, dispersos
    for x, y in [(120, 220), (740, 200), (180, 740), (740, 680)]:
        objs.append(worldObjects.getTree(x, y))
    # arbustos
    for x, y in [(260, 440), (560, 440), (400, 720)]:
        objs.append(worldObjects.getBush(x, y))
    # 3 mini-enemigos + 1 boss
    objs.append(worldObjects.getEnemyAt("crasheador", 240, 240))
    objs.append(worldObjects.getEnemyAt("pulgita", 600, 240))
    objs.append(worldObjects.getEnemyAt("conexion", 420, 620))
    objs.append(worldObjects.getBoss(x=400, y=400))
    # portal izquierdo: vuelve a isla 1
    objs.append(worldObjects.Portal(
        x=80, y=430,
        targetIsland=1,
        targetSpawn=(720, 440),
        direction="left"
    ))
    return {
        "background": "assets/island2-bg.png",
        "objects": objs,
        "defaultSpawn": (140, 460),
    }
