import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

game = Game.objects.first()
with open('game_url.txt', 'w') as f:
    if game:
        f.write(game.image_url)
    else:
        f.write("No games found")
