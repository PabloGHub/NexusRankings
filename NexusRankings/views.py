from django.shortcuts import render

from .forms import *
from .models import *

# Create your views here.
def listar_nexusrankings(request):
    datos:Game = Game.objects.all()
    context = {'datos' : datos}
    return render(request, 'ranqueo/lista.html', context)

def registrarse(request):
    if (request.method == 'POST'):
        datosFormulario = RegistrarForm(request.POST)

        return render(request, 'ranqueo/inicio.html')
    else:
        context = {'datos' : {
            "accionNom" : "Registrarse",
            "accionTipo" : 0,
            "form" : RegistrarForm()
        }}
        return render(request, 'ranqueo/sesion.html', context)

def loguearse(request):
    context = {'datos': {
        "accionNom": "Iniciar Sesión",
        "accionTipo" : 1,
        "form": LoguearForm()
    }}

    return render(request, 'ranqueo/sesion.html', context)

def inicio(request):
    return render(request, 'ranqueo/inicio.html')