import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game
print(f"Total Games: {Game.objects.count()}")
for game in Game.objects.all():
    print(f"- {game.title} | Genre: '{game.genre}' | Price: {game.price}")
