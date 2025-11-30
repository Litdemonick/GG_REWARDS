import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

games = Game.objects.all()
print(f"Found {games.count()} games.")
for game in games:
    print(f"Game: {game.title}, Image URL: '{game.image_url}'")
