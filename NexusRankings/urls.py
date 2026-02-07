from django.urls import path
from NexusRankings import views

urlpatterns = [
    path('', views.inicio, name='index'),
    path('listarGames/', views.listarGames, name='listarGames'),
    path('registrarse/', views.registrarse, name='registrarse'),
    path('loguearse/', views.loguearse, name='loguearse'),
    path('desLoguearse/', views.desLoguearse, name='desLoguearse'),
    path('listarMods/<int:game_id>/', views.listarMods, name='listarMods'),
    path('importarGames/', views.importarGames, name='importarGames'),
    path('importarMods/', views.importarMods, name='importarMods'),
    path('mod/<int:mod_id>/', views.reputacionMod, name='mod'),
    path('ranking/<int:game_id>/', views.ranking, name='ranking'),
    path('borrarGame/<int:game_id>/', views.borrarGame, name='borrarGame'),
    path('borrarMod/<int:mod_id>/', views.borrarMod, name='borrarMod'),
    path("administracion/", views.admin, name="admin"),
    path("estadisticasGame/<int:game_id>/", views.estadisticasGame, name="estadisticasGame"),
    path("estadisticasMod/<int:mod_id>/", views.estadisticasMod, name="estadisticasMod"),
    path("listarUsuarios/", views.listarUsuarios, name="listarUsuarios"),
    path("borrarUsuario/<int:user_id>/", views.borrarUsuario, name="borrarUsuario"),
]

