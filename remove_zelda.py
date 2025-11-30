import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

def remove_zelda():
    try:
        game = Game.objects.get(title="The Legend of Zelda: Tears of the Kingdom")
        game.delete()
        print("Successfully removed The Legend of Zelda: Tears of the Kingdom")
    except Game.DoesNotExist:
        print("The Legend of Zelda: Tears of the Kingdom does not exist in the database")
    except Exception as e:
        print(f"Error removing game: {e}")

if __name__ == '__main__':
    remove_zelda()
