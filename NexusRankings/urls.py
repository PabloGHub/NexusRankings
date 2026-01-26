from django.urls import path
from NexusRankings import views

urlpatterns = [
    path('', views.inicio, name='index'),
    path('listarGames/', views.listarGames, name='listarGames'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('loguearse/', views.loguearse, name='loguearse'),
    path('desLoguearse/', views.desLoguearse, name='desLoguearse'),
]

