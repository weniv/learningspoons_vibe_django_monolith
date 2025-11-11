# game/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Player, Item, GameSession, PlayerScore


def index(request):
    """게임 메인 페이지"""
    return render(request, "game/index.html")


def start_game(request):
    """게임 시작"""
    if request.method == "POST":
        session = GameSession.objects.create(session_name="New Game")
        # 3명의 플레이어 생성
        players = []
        colors = ["red", "blue", "green"]
        for i, color in enumerate(colors):
            player = Player.objects.create(name=f"Player {i+1}", color=color)
            session.players.add(player)
            players.append(
                {"id": player.id, "name": player.name, "color": player.color}
            )
        return JsonResponse({"session_id": session.id, "players": players})
    return JsonResponse({"error": "Invalid request"}, status=400)


def score(request):
    """점수 확인"""
    scores = PlayerScore.objects.select_related("player", "game_session").order_by(
        "-total_score"
    )
    return render(request, "game/score.html", {"scores": scores})
