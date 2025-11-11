# game/models.py
from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default="red")  # 플레이어 색상
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    ITEM_TYPES = [
        ("tomato", "토마토"),
        ("lettuce", "양상추"),
        ("cheese", "치즈"),
        ("bread", "빵"),
        ("meat", "고기"),
    ]

    name = models.CharField(max_length=50)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    points = models.IntegerField(default=10)  # 아이템 점수

    def __str__(self):
        return self.name


class GameSession(models.Model):
    session_name = models.CharField(max_length=100)
    players = models.ManyToManyField(Player, related_name="game_sessions")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.session_name


class PlayerScore(models.Model):
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    items_collected = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    class Meta:
        unique_together = ["game_session", "player"]

    def __str__(self):
        return f"{self.player.name} - {self.total_score}"
