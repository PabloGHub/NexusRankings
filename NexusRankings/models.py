from django.db import models
try:
    from django_mongodb_backend.models import EmbeddedModel as Modelo
except Exception:
    Modelo = models.Model

# Create your models here.
class Game(models.Model):
    game_id:int = models.IntegerField(null=False, unique=True)
    name:str = models.CharField(max_length=100, null=False)
    nexusmods_url:str = models.CharField(max_length=200, null=False)
    mods:int = models.IntegerField(null=False)

    class Meta:
        db_table = 'game'
        managed = False

    def __str__(self):
        return self.name
    

class Mod(models.Model):
    mod_id:int = models.IntegerField(null=False, unique=True)
    game_id:int = models.IntegerField(null=False)
    name:str = models.CharField(max_length=200, null=False)
    summary:str = models.CharField(max_length=500, null=False)
    picture_url:str = models.CharField(max_length=200, null=False)
    author:str = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'mod'
        managed = False

    def __str__(self):
        return self.name


class usuario(models.Model):
    nombre:str = models.CharField(max_length=100, null=False, unique=True)
    contra:str = models.CharField(max_length=100, null=False)

    class Meta:
        pass

    def __str__(self):
        return self.nombre