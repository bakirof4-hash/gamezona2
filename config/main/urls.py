from django.urls import path
from . import views

urlpatterns = [
    path('healthz/', views.healthz, name='healthz'),
    path('', views.home, name='home'),
    path('account/', views.account, name='account'),
    path('account/logout/', views.account_logout, name='account_logout'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('keepalive/', views.keepalive, name='keepalive'),
    path('horror/', views.horror_home, name='horror_home'),
    path('horror/create/', views.horror_create_room, name='horror_create_room'),
    path('horror/join/', views.horror_join_room, name='horror_join_room'),
    path('horror/room/<str:code>/', views.horror_room, name='horror_room'),
    path('horror/api/room/<str:code>/', views.horror_room_state, name='horror_room_state'),
    path('horror/api/room/<str:code>/action/', views.horror_room_action, name='horror_room_action'),
    path('game/', views.game, name='game'),
    path('game/tiles/', views.game_tiles, name='game_tiles'),
    path('game/lanes/', views.game_lanes, name='game_lanes'),
    path('game/orbit/', views.game_orbit, name='game_orbit'),
    path('arcade/<slug:slug>/', views.arcade_game, name='arcade_game'),
    path('author', views.auth, name='author'),
    path('game2', views.hom2, name=''),
]
