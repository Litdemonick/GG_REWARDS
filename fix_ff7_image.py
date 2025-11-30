import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

def update_ff7():
    try:
        game = Game.objects.get(title="Final Fantasy VII Rebirth")
        # Correct App ID is 2909400
        game.link_url = "https://store.steampowered.com/app/2909400/FINAL_FANTASY_VII_REBIRTH/"
        game.image_url = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2909400/library_600x900.jpg"
        game.save()
        print(f"Updated FF7 Rebirth: Link={game.link_url}, Image={game.image_url}")
    except Game.DoesNotExist:
        print("Final Fantasy VII Rebirth not found")
    except Exception as e:
        print(f"Error updating FF7: {e}")

if __name__ == '__main__':
    update_ff7()
