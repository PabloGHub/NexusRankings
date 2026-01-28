from .AccesoJson import *

def cargarJuegos(archivo):
    decodificado = archivo.read().decode('utf-8')# .splitlines()
    n = listarJuegos(decodificado)
    for l in n:
        l.save(using="mongodb")

def cargarMods(archivo):
    decodificado = archivo.read().decode('utf-8')# .splitlines()
    n = listarMods(decodificado)
    for l in n:
        l.save(using="mongodb")