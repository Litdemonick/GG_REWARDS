import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

games = Game.objects.all()
with open('all_game_urls.txt', 'w', encoding='utf-8') as f:
    for game in games:
        f.write(f"{game.title}: {game.image_url}\n")
