from django.urls import path
from NexusRankings import views

urlpatterns = [
    path('', views.inicio, name='index'),
    path('lista/', views.listar_nexusrankings, name='lista'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('loguearse/', views.loguearse, name='loguearse'),
]

