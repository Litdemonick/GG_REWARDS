import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

game = Game.objects.first()
if game:
    print(f"Title: {game.title}")
    print(f"URL: {game.image_url}")
else:
    print("No games found.")
