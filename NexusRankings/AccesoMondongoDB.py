from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .models import *

def getGame(game_id:int):
    try:
        return Game.objects.using("mongodb").get(game_id=game_id)
    except MultipleObjectsReturned:
        return Game.objects.using("mongodb").filter(game_id=game_id).first()
    except ObjectDoesNotExist:
        return None

def getGames():
    datos = Game.objects.using("mongodb").all()
    return datos

def delGame(game_id:int):
    Game.objects.using("mongodb").filter(game_id=game_id).delete()


def getMod(mod_id:int):
    try:
        return Mod.objects.using("mongodb").get(mod_id=mod_id)
    except MultipleObjectsReturned:
        return Mod.objects.using("mongodb").filter(mod_id=mod_id).first()
    except ObjectDoesNotExist:
        return None

def getMods(game_id:int):
    datos = Mod.objects.using("mongodb").filter(game_id=game_id)
    return datos

def delMod(mod_id:int):
    Mod.objects.using("mongodb").filter(mod_id=mod_id).delete()


def getRanking(game_id:int, user_id:int):
    jogo:Game = getGame(game_id)
    if jogo:
        for r in (jogo.rankings or []):
            if r.user_id == user_id:
                return r
    return None

def guardarRanking(game_id:int, ranking:Ranking):
    jogo:Game = getGame(game_id)
    if jogo.rankings is None:
        jogo.rankings = []

    existing = next((r for r in jogo.rankings if r.user_id == ranking.user_id), None)
    if existing:
        existing.posiciones = ranking.posiciones
    else:
        jogo.rankings.append(ranking)

    Game.objects.using("mongodb").filter(game_id=game_id).update(rankings=jogo.rankings)

# mods que esten en la posicion x de los rankings.
def masPosicion(game_id:int, posicion:int = 1):
    jogo:Game = getGame(game_id)
    if jogo and jogo.rankings:
        count = {}
        for r in jogo.rankings:
            for p in r.posiciones:
                if p.position == posicion:
                    count[p.mod_id] = count.get(p.mod_id, 0) + 1

        return {'mod': max(count, key=count.get), 'count': max(count.values())}
    return None

def masPuntuacion(game_id:int, puntuacion:int = 1):
    mods = getMods(game_id)
    count = {}
    for mod in mods:
        for r in (mod.reputaciones or []):
            if r.score == puntuacion:
                count[mod.mod_id] = count.get(mod.mod_id, 0) + 1

    if count:
        return {'mod': max(count, key=count.get), 'count': max(count.values())}
    return None

# mods que tengan una puntuacion x en las reputaciones.
def conPuntuacion(game_id:int, puntuacion:int = 1):
    mods = getMods(game_id)
    count = {}
    for mod in mods:
        for r in (mod.reputaciones or []):
            if r.score == puntuacion:
                count[mod.mod_id] = count.get(mod.mod_id, 0) + 1

    return count


def estadisticaMod(mod_id:int):
    mod:Mod = getMod(mod_id)
    jogo:Game = getGame(mod.game_id)

    numJogo = {
        'pos1': 0,
        'pos2': 0,
        'pos3': 0,
        'pos4': 0,
        'pos5': 0,
    } # total veces aparecio en cada posicion.
    numMod = {
        'score1': 0,
        'score2': 0,
        'score3': 0,
        'score4': 0,
        'score5': 0,
    } # total veces aparecio en cada puntuacion.

    if jogo and jogo.rankings:
        for r in jogo.rankings:
            for p in r.posiciones:
                if p.mod_id == mod_id:
                    numJogo[f'pos{p.position}'] += 1

    if mod and mod.reputaciones:
        for r in mod.reputaciones:
            numMod[f'score{r.score}'] += 1

    return {
        'numJogo': numJogo,
        'numMod': numMod,
    }

def estadisticasUsuario(user_id:int):
    juegos = getGames()
    mods = []
    for jogo in juegos:
        if jogo.rankings:
            for r in jogo.rankings:
                if r.user_id == user_id:
                    mods.extend(r.posiciones)

    puntuaciones = {}
    for mod in mods:
        m = getMod(mod.mod_id)
        if m and m.reputaciones:
            for r in m.reputaciones:
                if r.user_id == user_id:
                    puntuaciones[mod.mod_id] = r.score

    return {
        'mods': mods,
        'puntuaciones': puntuaciones,
    }

def getCantidadMods(game_id:int):
    mods:list = getMods(game_id)
    return len(mods) if mods else 0

def getCantidadPuntuaciones(game_id:int):
    mods = getMods(game_id)
    count = 0
    for mod in mods:
        count += len(mod.reputaciones or [])
    return count

def getCantidadRankings(game_id:int):
    jogo:Game = getGame(game_id)
    return len(jogo.rankings or []) if jogo else 0

def getCantidadTotalMods():
    return Game.objects.using("mongodb").aggregate(models.Count('mods'))[0]['mods__count']