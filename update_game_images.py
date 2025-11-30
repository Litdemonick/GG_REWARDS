import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

def update_images():
    games = {
        "Cyberpunk 2077": "1091500",
        "Hollow Knight: Silksong": "1030300",
        "Elden Ring": "1245620",
        "God of War Ragnarök": "2322010",
        "Baldur's Gate 3": "1086940",
        "Final Fantasy VII Rebirth": "2930160",
        "Black Myth: Wukong": "2358720"
    }

    for title, app_id in games.items():
        image_url = f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{app_id}/library_600x900.jpg"
        try:
            game = Game.objects.get(title=title)
            game.image_url = image_url
            game.save()
            print(f"Updated image for {title}: {image_url}")
        except Game.DoesNotExist:
            print(f"Game not found: {title}")
        except Exception as e:
            print(f"Error updating {title}: {e}")

if __name__ == '__main__':
    update_images()
