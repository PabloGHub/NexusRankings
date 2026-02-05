from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from .models import *

def getGame(game_id:int):
    jogo:Game = Game.objects.using("mongodb").get(game_id=game_id)
    try:
        return jogo
    except MultipleObjectsReturned:
        return jogo.first()
    except ObjectDoesNotExist:
        return None

def getGames():
    datos = Game.objects.using("mongodb").all()
    return datos



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