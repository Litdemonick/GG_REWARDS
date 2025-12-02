import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

games = Game.objects.all()[:5]
print(f"Checking {len(games)} games...")
for game in games:
    print(f"Title: {game.title}")
    print(f"Image URL: {game.image_url}")
    print("-" * 20)
