# game/urls.py (새로 생성)
from django.urls import path
from . import views

app_name = "game"

urlpatterns = [
    path("", views.index, name="index"),
    path("start/", views.start_game, name="start_game"),
    path("score/", views.score, name="score"),
]
