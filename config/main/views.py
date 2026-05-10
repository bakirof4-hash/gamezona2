import json
import random
import string

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .models import HorrorPresence, HorrorRoom, Score


NEW_ARCADE_GAMES = [
    {"slug": "prism-drift", "title": "Prism Drift", "genre": "Dodge", "tagline": "Neon lazerlar orasidan sirg'alib o'ting.", "description": "Sichqoncha bilan hovercraftni boshqarib, rangli prismalardan qoching va combo yig'ing.", "accent": "#7cf6ff"},
    {"slug": "meteor-pop", "title": "Meteor Pop", "genre": "Clicker", "tagline": "Portlashdan oldin meteorlarni yo'q qiling.", "description": "Tez reaction kerak: ekranda paydo bo'lgan obyektlarni vaqt tugashidan oldin bosing.", "accent": "#ff8a5b"},
    {"slug": "ring-rescue", "title": "Ring Rescue", "genre": "Collect", "tagline": "Yadro atrofida halqalarni yig'ing.", "description": "Markaz atrofida siljib, oltin halqalarni olib qizil zonalardan qoching.", "accent": "#ffe27a"},
    {"slug": "gravity-well", "title": "Gravity Well", "genre": "Orbit", "tagline": "Gravitatsiya markazidan chiqib ketmang.", "description": "WASD bilan zondni boshqarib, markaziy tortishish va chiqindilar bilan kurashing.", "accent": "#8b7cff"},
    {"slug": "tower-balance", "title": "Tower Balance", "genre": "Stack", "tagline": "Har blokni mukammal tushiring.", "description": "Harakatlanayotgan bloklarni drop qilib, osmoni tower yasang. Xato qilsangiz platforma torayadi.", "accent": "#7dffb5"},
    {"slug": "color-rush", "title": "Color Rush", "genre": "Match", "tagline": "Yo'lak va rangni bir vaqtda moslang.", "description": "Chap-o'ng harakat va rang almashtirishni birlashtirib, darvozalardan o'ting.", "accent": "#ff5db1"},
    {"slug": "drift-breaker", "title": "Drift Breaker", "genre": "Breaker", "tagline": "Neon devorlarni parchalab tashlang.", "description": "Klassik brick breakerning silliq, yuqori kontrastli arcade talqini.", "accent": "#59d7ff"},
    {"slug": "shadow-step", "title": "Shadow Step", "genre": "Stealth", "tagline": "Spotlightdan tashqarida qoling.", "description": "Kursoringizni xavfsiz joylarda ushlab, skaner nurlaridan qoching.", "accent": "#c4b5fd"},
    {"slug": "crystal-harvest", "title": "Crystal Harvest", "genre": "Gather", "tagline": "Kristallarni yig'ib, minalardan qoching.", "description": "Arena ichida yurib, tez-tez respawn bo'ladigan kristallarni tering.", "accent": "#5fffcf"},
    {"slug": "arc-blaster", "title": "Arc Blaster", "genre": "Shooter", "tagline": "Yuqoridan tushayotgan dronlarni uring.", "description": "To'pni burib, projectiles bilan osmondan yog'ilayotgan nishonlarni tushiring.", "accent": "#ffcf6d"},
    {"slug": "aurora-link", "title": "Aurora Link", "genre": "Puzzle", "tagline": "Yorqin tugunlarni to'g'ri tartibda ulang.", "description": "Combo bilan chiziqlar chizing, noto'g'ri ulanish esa energiyani pasaytiradi.", "accent": "#6ef3d6"},
    {"slug": "zen-pulse", "title": "Zen Pulse", "genre": "Timing", "tagline": "Bosimni target zonada qo'ying.", "description": "Hold va release asosida ishlovchi sokin, lekin aniq timing o'yini.", "accent": "#8fd2ff"},
    {"slug": "nova-jump", "title": "Nova Jump", "genre": "Runner", "tagline": "Kosmik runnerda to'siqlardan sakrang.", "description": "Bir tugmali endless run, ammo parallax va particle bilan ancha jonli.", "accent": "#ffa26e"},
    {"slug": "sky-hook", "title": "Sky Hook", "genre": "Swing", "tagline": "Arqondan bo'shab platformaga qo'ning.", "description": "Pendulum momentini to'g'ri topib, bir platformadan boshqasiga o'ting.", "accent": "#82f7ff"},
]

HORROR_LOCATIONS = [
    {"slug": "abandoned-hospital", "title": "Abandoned Hospital", "mood": "Sovuq neon koridorlar va qon hidi.", "accent": "#7df9ff"},
    {"slug": "forest-chapel", "title": "Forest Chapel", "mood": "Tumandagi cherkov va g'ichirlagan yog'och.", "accent": "#8fff87"},
    {"slug": "metro-tunnel", "title": "Metro Tunnel", "mood": "Signal uzilgan tunellar va uzoqdan kelgan ovozlar.", "accent": "#ffcf5a"},
    {"slug": "mirror-hotel", "title": "Mirror Hotel", "mood": "Cheksiz oynalar va noto'g'ri akslar.", "accent": "#ff7d9a"},
]

SCREAMERS = [
    {"slug": "nun", "title": "Silent Nun", "text": "Behind you. Do not blink."},
    {"slug": "crawler", "title": "Vent Crawler", "text": "It knows your room code now."},
    {"slug": "static-face", "title": "Static Face", "text": "The screen should not have eyes."},
    {"slug": "red-mist", "title": "Red Mist", "text": "Run. It is already inside."},
]

ACCENTS = ["#ff5c75", "#7df9ff", "#9b87ff", "#ffcf5a", "#78ffb5", "#ff9d6b"]


def ensure_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def make_room_code():
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not HorrorRoom.objects.filter(code=code).exists():
            return code


def location_map():
    return {item["slug"]: item for item in HORROR_LOCATIONS}


def screamer_map():
    return {item["slug"]: item for item in SCREAMERS}


def build_game_library():
    existing_games = [
        {"slug": "nebula-rush", "title": "Nebula Rush", "genre": "Arcade", "tagline": "Kosmik survival va pulse combat.", "description": "Meteor, kristall va combo bilan boyitilgan flying arcade.", "accent": "#ffd166", "href": reverse("game"), "is_new": False},
        {"slug": "flash-tiles", "title": "Flash Tiles", "genre": "Memory", "tagline": "Ketma-ketlikni yodda saqlang.", "description": "Qisqa pattern eslab qolish va tez javob qaytarish o'yini.", "accent": "#4cc9f0", "href": reverse("game_tiles"), "is_new": False},
        {"slug": "lane-escape-nitro", "title": "Lane Escape Nitro", "genre": "Reflex", "tagline": "Neon trassada mashinalardan qoching.", "description": "3 lane dodge, shield va oshib boruvchi nitro tezligi bilan.", "accent": "#ff2f92", "href": reverse("game_lanes"), "is_new": False},
        {"slug": "orbit-tap", "title": "Orbit Tap", "genre": "Timing", "tagline": "Orbni oltin segment bilan tekislang.", "description": "Minimal, ammo tez qiyinlashadigan timing challenge.", "accent": "#7bdff2", "href": reverse("game_orbit"), "is_new": False},
        {"slug": "horror-rooms", "title": "Horror Rooms", "genre": "Multiplayer", "tagline": "Kod bilan do'stingizni qorong'i xonaga olib kiring.", "description": "Alohida horror bo'lim: room code, lokatsiyalar va scrimer trigger.", "accent": "#ff5c75", "href": reverse("horror_home"), "is_new": True},
    ]
    new_games = [{**game, "href": reverse("arcade_game", kwargs={"slug": game["slug"]}), "is_new": True} for game in NEW_ARCADE_GAMES]
    return existing_games + new_games


def room_payload(room, viewer_session):
    players = list(room.players.order_by("joined_at"))
    location = location_map().get(room.location, HORROR_LOCATIONS[0])
    return {
        "code": room.code,
        "name": room.name,
        "location": location,
        "atmosphere": room.atmosphere,
        "screamer": room.screamer,
        "screamer_text": room.screamer_text,
        "is_host": room.host_session == viewer_session,
        "players": [
            {
                "nickname": player.nickname,
                "accent": player.accent,
                "is_host": room.host_session == player.session_key,
                "is_me": player.session_key == viewer_session,
            }
            for player in players
        ],
    }


def upsert_presence(room, session_key, nickname):
    presence, _ = HorrorPresence.objects.update_or_create(
        room=room,
        session_key=session_key,
        defaults={"nickname": nickname[:40], "accent": random.choice(ACCENTS)},
    )
    return presence


def home(request):
    games = build_game_library()
    return render(request, "index.html", {"games": games, "featured_games": games[:6], "new_games_count": len(NEW_ARCADE_GAMES), "total_games_count": len(games)})


def game(request):
    return render(request, "game.html")


def game_tiles(request):
    return render(request, "game_tiles.html")


def game_lanes(request):
    return render(request, "game_lanes.html")


def game_orbit(request):
    return render(request, "game_orbit.html")


def arcade_game(request, slug):
    game_map = {game["slug"]: game for game in NEW_ARCADE_GAMES}
    game_data = game_map.get(slug)
    if not game_data:
        raise Http404("Game not found")
    return render(request, "game_arcade.html", {"game": game_data, "games": build_game_library()})


def auth(request):
    return render(request, "author.html")


def hom2(request):
    top = Score.objects.order_by("-score")[:10]
    return render(request, "home.html", {"top": top, "games": build_game_library()})


def leaderboard(request):
    top = Score.objects.order_by("-score")[:10]
    return render(request, "leaderboard.html", {"top": top})


def horror_home(request):
    return render(request, "horror_home.html", {"locations": HORROR_LOCATIONS, "screamers": SCREAMERS})


@require_POST
def horror_create_room(request):
    session_key = ensure_session(request)
    nickname = (request.POST.get("nickname") or "Ghost").strip()[:40]
    room_name = (request.POST.get("room_name") or "Midnight Room").strip()[:120]
    location = request.POST.get("location") or HORROR_LOCATIONS[0]["slug"]
    if location not in location_map():
        location = HORROR_LOCATIONS[0]["slug"]
    room = HorrorRoom.objects.create(code=make_room_code(), name=room_name, location=location, host_session=session_key, atmosphere="The room is listening.")
    upsert_presence(room, session_key, nickname)
    request.session["horror_nickname"] = nickname
    return redirect("horror_room", code=room.code)


@require_POST
def horror_join_room(request):
    session_key = ensure_session(request)
    code = (request.POST.get("code") or "").strip().upper()
    nickname = (request.POST.get("nickname") or "Ghost").strip()[:40]
    room = get_object_or_404(HorrorRoom, code=code)
    upsert_presence(room, session_key, nickname)
    request.session["horror_nickname"] = nickname
    return redirect("horror_room", code=room.code)


def horror_room(request, code):
    session_key = ensure_session(request)
    room = get_object_or_404(HorrorRoom, code=code.upper())
    nickname = request.session.get("horror_nickname")
    if nickname:
        upsert_presence(room, session_key, nickname)
    presence = room.players.filter(session_key=session_key).first()
    return render(request, "horror_room.html", {"room": room, "presence": presence, "room_json": room_payload(room, session_key), "locations": HORROR_LOCATIONS, "screamers": SCREAMERS})


@require_GET
def horror_room_state(request, code):
    session_key = ensure_session(request)
    room = get_object_or_404(HorrorRoom, code=code.upper())
    if not room.players.filter(session_key=session_key).exists():
        return JsonResponse({"error": "forbidden"}, status=403)
    return JsonResponse(room_payload(room, session_key))


@require_POST
def horror_room_action(request, code):
    session_key = ensure_session(request)
    room = get_object_or_404(HorrorRoom, code=code.upper())
    if not room.players.filter(session_key=session_key).exists():
        return JsonResponse({"error": "forbidden"}, status=403)
    payload = json.loads(request.body or "{}")
    action = payload.get("action")
    if action == "set_location":
        if session_key != room.host_session:
            return JsonResponse({"error": "host_only"}, status=403)
        location = payload.get("location")
        if location in location_map():
            room.location = location
            room.atmosphere = location_map()[location]["mood"]
    elif action == "trigger_screamer":
        if session_key != room.host_session:
            return JsonResponse({"error": "host_only"}, status=403)
        screamer = payload.get("screamer")
        if screamer in screamer_map():
            room.screamer = screamer
            room.screamer_text = screamer_map()[screamer]["text"]
    elif action == "clear_screamer":
        room.screamer = ""
        room.screamer_text = ""
    elif action == "set_atmosphere":
        atmosphere = (payload.get("atmosphere") or "").strip()[:220]
        if atmosphere:
            room.atmosphere = atmosphere
    room.save()
    return JsonResponse(room_payload(room, session_key))


def save_score(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if not request.user.is_authenticated:
            return JsonResponse({"status": "auth_required"}, status=403)
        Score.objects.create(user=request.user, game_name=data["game"], score=data["score"])
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=405)
