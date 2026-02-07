from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .models import *

def getGame(game_id:int):
    try:
        jogo:Game = Game.objects.using("mongodb").get(game_id=game_id)
        return jogo
    except MultipleObjectsReturned:
        return jogo.first()
    except ObjectDoesNotExist:
        return None

def getGames():
    datos = Game.objects.using("mongodb").all()
    return datos

def delGame(game_id:int):
    Game.objects.using("mongodb").filter(game_id=game_id).delete()


def getMod(mod_id:int):
    mod:Mod = Mod.objects.using("mongodb").get(mod_id=mod_id)
    try:
        return mod
    except MultipleObjectsReturned:
        return mod.first()
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

# mods que tengan una puntuacion x en las reputaciones.
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