from django.shortcuts import render

from .forms import *
from .models import *

# Create your views here.
def listar_nexusrankings(request):
    datos = Game.objects.using("mongodb").all()
    context = {'datos' : datos}
    return render(request, 'ranqueo/lista.html', context)


def __ir_registro(request, form:RegistrarForm):
    context = {'datos': {
        "accionNom": "Registrarse",
        "accionTipo" : 0,
        "form": form
    }}
    return render(request, 'ranqueo/sesion.html', context)
def registrarse(request):
    if (request.method == 'POST'):
        datosFormulario:RegistrarForm = RegistrarForm(request.POST)

        if datosFormulario.is_valid():
            contra = datosFormulario.cleaned_data.get('contra')
            contra2 = datosFormulario.cleaned_data.get('contra2')

            if contra != contra2:
                return __ir_registro(request, datosFormulario)

            user = datosFormulario.save(commit=False)
            user.set_password(datosFormulario.cleaned_data['contra'])
            user.save()
            return render(request, 'ranqueo/inicio.html')
        else:
            return __ir_registro(request, datosFormulario)
    else:
        return __ir_registro(request, RegistrarForm())


def __ir_logueo(request, form:LoguearForm):
    context = {'datos': {
        "accionNom": "Iniciar Sesión",
        "accionTipo" : 1,
        "form": form
    }}
    return render(request, 'ranqueo/sesion.html', context)
def loguearse(request):

    return __ir_logueo(request, LoguearForm())

def inicio(request):
    return render(request, 'ranqueo/inicio.html')