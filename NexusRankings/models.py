from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django_mongodb_backend.models import *
from django_mongodb_backend.fields import *

# try:
#     from django_mongodb_backend.models import EmbeddedModel as Modelo
# except Exception:
#     Modelo = models.Model

# Create your models here.
class Posicion(EmbeddedModel):
    mod_id:int = models.IntegerField(null=False)
    position:int = models.IntegerField(null=False)

class Ranking(EmbeddedModel):
    user_id:int = models.IntegerField(null=False)
    posiciones:list = EmbeddedModelArrayField(Posicion, null=True, blank=True)

class Game(models.Model):
    game_id:int = models.IntegerField(null=False, unique=True)
    name:str = models.CharField(max_length=100, null=False, unique=True)
    nexusmods_url:str = models.CharField(max_length=200, null=False)
    mods:int = models.IntegerField(null=False)
    rankings:list = EmbeddedModelArrayField(Ranking, null=True, blank=True)
    maxPosRankings:int = models.IntegerField(null=False, default=5)

    class Meta:
        db_table = 'game'
        managed = False

    def __str__(self):
        return self.name


class Reputacion(EmbeddedModel):
    user_id:int = models.IntegerField(null=False)
    score:int = models.IntegerField(null=False) # 0 -> 5
    summary:str = models.CharField(max_length=300, null=False)

class Mod(models.Model):
    mod_id:int = models.IntegerField(null=False, unique=True)
    game_id:int = models.IntegerField(null=False)
    name:str = models.CharField(max_length=200, null=False, unique=True)
    summary:str = models.CharField(max_length=500, null=False)
    picture_url:str = models.CharField(max_length=200, null=False)
    author:str = models.CharField(max_length=100, null=False)
    reputaciones:list = EmbeddedModelArrayField(Reputacion, null=True, blank=True)

    class Meta:
        db_table = 'mod'
        managed = False

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Debes rellenar los campos requeridos (username)")
        user = self.model(nombre=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre:str = models.CharField(max_length=100, null=False, unique=True)
    password: str = models.CharField(max_length=128, default='') # Esto no tiene ningun puto sentido.
    # super:bool = models.BooleanField(default=False)
    is_active:bool = models.BooleanField(default=True)
    is_staff:bool = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'nombre'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nombre