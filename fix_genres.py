import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

for game in Game.objects.all():
    original_genre = game.genre
    cleaned_genre = game.genre.strip()
    if original_genre != cleaned_genre:
        game.genre = cleaned_genre
        game.save()
        print(f"Fixed genre for {game.title}: '{original_genre}' -> '{cleaned_genre}'")
    else:
        print(f"Genre for {game.title} is clean: '{game.genre}'")
