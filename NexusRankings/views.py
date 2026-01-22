from django.shortcuts import render
from .models import Game

# Create your views here.
def listar_nexusrankings(request):
    datos:Game = Game.objects.all()
    context = {'datos' : datos}
    return render(request, 'ranqueo/lista.html', context)