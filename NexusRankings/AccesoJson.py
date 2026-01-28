import json
from .models import Game, Mod

def darme(archivo):
    return json.loads(archivo)

def crearJuego(dato):
    return Game(
        game_id = int(dato["game_id"]),
        name = str(dato["name"]),
        nexusmods_url = str(dato["nexusmods_url"]),
        mods = int(dato["mods"])
        )

def crearJuegos(datos):
    _lista = []
    for _j in datos:
        _novoJuego = crearJuego(_j)
        _lista.append(_novoJuego)
    return _lista

def listarJuegos(archivo):
    _juegos = darme(archivo)
    return crearJuegos(_juegos)

def crearMod(dato):
    return Mod(
        mod_id = int(dato["mod_id"]),
        game_id = int(dato["game_id"]),
        name = str(dato["name"]),
        summary = str(dato["summary"]),
        picture_url = str(dato["picture_url"]),
        author = str(dato["author"])
    )

def crearMods(datos):
    _lista = []
    for _j in datos:
        _novoMod = crearMod(_j)
        _lista.append(_novoMod)
    return _lista

def listarMods(archivo):
    _mods = darme(archivo)
    return crearMods(_mods)