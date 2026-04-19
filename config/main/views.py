from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def game(request):
    return render(request, "game.html")


def game_tiles(request):
    return render(request, "game_tiles.html")


def game_lanes(request):
    return render(request, "game_lanes.html")


def game_orbit(request):
    return render(request, "game_orbit.html")
