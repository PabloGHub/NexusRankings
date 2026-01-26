class CargadorJson:
    import json

    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def cargar_datos(self):
        with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
            datos = self.json.load(archivo)
        return datos