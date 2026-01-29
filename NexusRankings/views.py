from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render

from .CargadorJson import *

from .forms import *
from .models import *

# Create your views here.
def inicio(request):
    return render(request, 'ranqueo/inicio.html')

def __ir_lista(request, context):
    if request.user.is_authenticated:
        return render(request, 'ranqueo/lista.html', context)
    else:
        return inicio(request)

def listarGames(request):
    datos = Game.objects.using("mongodb").all()
    context = {'datos' : {
        "tipo": "Juegos",
        "accion" : 0,
        "items": datos
    }}
    return __ir_lista(request, context)

def listarMods(request, game_id):
    datos = Mod.objects.using("mongodb").filter(game_id=game_id)
    context = {'datos': {
        "tipo": "Mods",
        "accion" : 1,
        "items": datos
    }}
    return __ir_lista(request, context)

def __ir_sesion(request, context):
    if request.user.is_authenticated:
        return inicio(request)
    else:
        return render(request, 'ranqueo/sesion.html', context)

def __ir_registro(request, form:RegistrarForm):
    context = {'datos': {
        "accionNom": "Registrarse",
        "accionTipo" : 0,
        "form": form
    }}
    return __ir_sesion(request, context)

def __registrarse(request, datosFormulario):
    if datosFormulario.is_valid():
        contra = datosFormulario.cleaned_data.get('contra')
        contra2 = datosFormulario.cleaned_data.get('contra2')

        if contra != contra2:
            return __ir_registro(request, datosFormulario)

        user = datosFormulario.save(commit=False)
        user.set_password(datosFormulario.cleaned_data['contra'])
        user.save()
        return inicio(request)
    else:
        return __ir_registro(request, datosFormulario)

def registrarse(request):
    if (request.method == 'POST'):
        datosFormulario:RegistrarForm = RegistrarForm(request.POST)
        return __registrarse(request, datosFormulario)
    else:
        return __ir_registro(request, RegistrarForm())

def __ir_logueo(request, form:LoguearForm):
    context = {'datos': {
        "accionNom": "Iniciar Sesión",
        "accionTipo" : 1,
        "form": form
    }}
    return render(request, 'ranqueo/sesion.html', context)

def __loguearse(request, datosFormulario):
    if datosFormulario.is_valid():
        nombre = datosFormulario.cleaned_data.get('username')
        contra = datosFormulario.cleaned_data.get('password')
        user = authenticate(request, username=nombre, password=contra)
        if user is not None:
            login(request, user)
            return listarGames(request)
    return __ir_logueo(request, datosFormulario)

def loguearse(request):
    if (request.method == 'POST'):
        datosFormulario:LoguearForm = LoguearForm(request, data=request.POST)
        return __loguearse(request, datosFormulario)
    else:
        return __ir_logueo(request, LoguearForm())

def desLoguearse(request):
    logout(request)
    return inicio(request)

def handler404(request, exception):
    return render(request, 'e404.html', status=404)


def __ir_importacion(request, context):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, 'ranqueo/importar.html', context)
    else:
        return inicio(request)

def __importarJuegos(request, context):
    arsivo = request.FILES.get('js_file')
    if arsivo is not None:
        cargarJuegos(arsivo)

    return __ir_importacion(request, context)

def importarGames(request):
    context = {'datos' : {
        "tipo": "Juegos",
        "accion" : 0
    }}
    if request.method == "POST":
        return __importarJuegos(request, context)
    else:
        return __ir_importacion(request, context)


def __importarMods(request, context):
    arsivo = request.FILES.get('js_file')
    if arsivo is not None:
        cargarMods(arsivo)

    return __ir_importacion(request, context)

def importarMods(request):
    context = {'datos' : {
        "tipo": "Mods",
        "accion" : 1
    }}
    if request.method == "POST":
        return __importarMods(request, context)
    else:
        return __ir_importacion(request, context)

def __ir_reputacionMod(request, context):
    if request.user.is_authenticated:
        return render(request, 'ranqueo/reputacion.html', context)
    else:
        return inicio(request)

def reputacionMod(request, mod_id):
    mod = Mod.objects.using("mongodb").get(mod_id=mod_id)
    form = mod.reputaciones.filter(user_id=request.user.id).first()
    if form is None: form = ReputacionForm()

    context = {'datos' : {
        "modName": mod.name,
        "form": form
    }}
    return __ir_reputacionMod(request, context)