from django.shortcuts import render

# Create your views here.
def listar_nexusrankings(request):
    return render(request, 'ranqueo/lista.html')