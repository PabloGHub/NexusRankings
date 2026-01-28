import json
from models import Game, Mod

class AccesoJson:
    def __init__(self, ruta):
        self.ruta = ruta

    def darme(self):
        with open(self.ruta, "r") as archivo:
            return json.load(archivo)

    def dar(self, datos):
        with open(self.ruta, "w") as archivo:
            json.dump(datos, archivo, indent=4)   


    def crearJuegos(self, datos):
        _lista = []
        for _j in datos:
            _novoJuego = Game(
                int(_j["game_id"]),
                str(_j["name"]),
                str(_j["nexusmods_url"]),
                int(_j["mods"])
                )
            _lista.append(_novoJuego)
        return _lista

    def listarJuegos(self):
        _juegos = self.darme()
        return self.crearJuegos(_juegos)


    def crearMods(self, datos):
        _lista = []
        for _j in datos:
            _novoMods = Mod(
                int(_j["mod_id"]),
                int(_j["game_id"]),
                str(_j["name"]),
                str(_j["summary"]),
                str(_j["picture_url"]),
                str(_j["author"])
                )
            _lista.append(_novoMods)
        return _lista

    def listarMods(self):
        _mods = self.darme()
        return self.crearMods(_mods)