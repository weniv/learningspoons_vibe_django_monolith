# game/routing.py (새로 생성)
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/game/", consumers.GameConsumer.as_asgi()),
]
