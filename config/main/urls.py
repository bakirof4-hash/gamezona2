from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('game/tiles/', views.game_tiles, name='game_tiles'),
    path('game/lanes/', views.game_lanes, name='game_lanes'),
    path('game/orbit/', views.game_orbit, name='game_orbit'),
    path('author', views.auth, name='author'),
    path('game2', views.hom2, name=''),
]
