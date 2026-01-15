from django.urls import path
from NexusRankings import views

urlpatterns = [
    path('', views.listar_nexusrankings, name='index'),
]
