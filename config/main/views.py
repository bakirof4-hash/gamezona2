from django.http import JsonResponse
from django.shortcuts import render, redirect


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

def auth(request):
    return render(request, "author.html")



def hom2(request):
    return render(request, "home.html")

from django.shortcuts import render
from .models import Score

def leaderboard(request):
    top = Score.objects.order_by('-score')[:10]
    return render(request, "leaderboard.html", {"top": top})

import json
from django.http import JsonResponse
from .models import Score

def save_score(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Score.objects.create(
            user=request.user,
            game_name=data["game"],
            score=data["score"]
        )

        return JsonResponse({"status": "ok"})