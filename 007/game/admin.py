# game/admin.py
from django.contrib import admin
from .models import Player, Item, GameSession, PlayerScore

admin.site.register(Player)
admin.site.register(Item)
admin.site.register(GameSession)
admin.site.register(PlayerScore)
