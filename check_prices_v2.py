import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

titles = [
    "Hollow Knight: Silksong",
    "Final Fantasy VII Rebirth",
    "Cyberpunk 2077",
    "Elden Ring",
    "Baldur's Gate 3"
]

games = Game.objects.filter(title="Hollow Knight: Silksong")
for game in games:
    print(f"{game.title} | ${game.price}")
