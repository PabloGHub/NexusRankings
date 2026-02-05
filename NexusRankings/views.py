from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseBadRequest

from .AccesoMondongoDB import *
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
    datos = getGames()
    context = {'datos' : {
        "tipo": "Juegos",
        "accion" : 0,
        "items": datos
    }}
    return __ir_lista(request, context)

def listarMods(request, game_id):
    datos = getMods(game_id)
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
        return render(request, 'ranqueo/mod.html', context)
    else:
        return inicio(request)


def __mostrarReputacionMod(request, mod:Mod):
    form:ReputacionForm = ReputacionForm()

    rep:Reputacion = next(
        (r for r in (mod.reputaciones or []) if r.user_id == request.user.id),
        None
    )

    form.fields['score'].initial = rep.score if rep else None
    form.fields['summary'].initial = rep.summary if rep else None

    context = {'datos': {
        "modName": mod.name,
        "form": form
    }}
    return __ir_reputacionMod(request, context)

def __guardarReputacionMod(request, mod:Mod, datosFormulario:ReputacionForm):
    if datosFormulario.is_valid():
        score = datosFormulario.cleaned_data.get('score')
        summary = datosFormulario.cleaned_data.get('summary')

        rep:Reputacion = next(
            (r for r in (mod.reputaciones or []) if r.user_id == request.user.id),
            None
        )

        if rep:
            rep.score = score
            rep.summary = summary
        else:
            nuevaRep = Reputacion(
                user_id = request.user.id,
                score = score,
                summary = summary
            )
            if mod.reputaciones is None:
                mod.reputaciones = []
            mod.reputaciones.append(nuevaRep)

        # Actualizar solo el campo 'reputaciones' en la DB para evitar un insert accidental
        Mod.objects.using("mongodb").filter(mod_id=mod.mod_id).update(reputaciones=mod.reputaciones)
        return __mostrarReputacionMod(request, mod)

    return __mostrarReputacionMod(request, mod)

def reputacionMod(request, mod_id):
    mod = Mod.objects.using("mongodb").get(mod_id=mod_id)
    if request.method == "POST":
        datosFormulario:ReputacionForm = ReputacionForm(request.POST)
        return __guardarReputacionMod(request, mod, datosFormulario)
    else:
        return __mostrarReputacionMod(request, mod)


def __ir_ranking(request, context):
    if request.user.is_authenticated:
        return render(request, 'ranqueo/ranking.html', context)
    else:
        return inicio(request)

def __mostrarRanking(request, game_id):
    jogo:Game = getGame(game_id)
    mods = getMods(game_id)

    context = {'datos': {
        "gameName": jogo.name,
        "game": jogo,
        "mods": mods,
    }}
    return __ir_ranking(request, context)

def __guardarRanking(request, game_id):
    jogo:Game = Game.objects.using("mongodb").get(game_id=game_id)

    try:
        pld = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return HttpResponseBadRequest('JSON inválido')

def ranking(request, game_id):
    if request.method == "POST":
        __guardarRanking(request, game_id)

    return __mostrarRanking(request, game_id)