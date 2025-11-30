import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

def update_games():
    updates = {
        "Cyberpunk 2077": {
            "link_url": "https://store.steampowered.com/app/1091500/Cyberpunk_2077/",
            "price": Decimal("20.99"),
            "discount": 65
        },
        "Hollow Knight: Silksong": {
            "link_url": "https://store.steampowered.com/app/1030300/Hollow_Knight_Silksong/",
            "price": Decimal("19.99"),
            "discount": 0
        },
        "Elden Ring": {
            "link_url": "https://store.steampowered.com/app/1245620/ELDEN_RING/",
            "price": Decimal("59.99"),
            "discount": 0
        },
        "God of War Ragnarök": {
            "link_url": "https://store.steampowered.com/app/2322010/God_of_War_Ragnark/",
            "price": Decimal("47.99"),
            "discount": 20
        },
        "Baldur's Gate 3": {
            "link_url": "https://store.steampowered.com/app/1086940/Baldurs_Gate_3/",
            "price": Decimal("59.99"),
            "discount": 0
        },
        "Final Fantasy VII Rebirth": {
            "link_url": "https://store.steampowered.com/app/2930160/FINAL_FANTASY_VII_REBIRTH/", # Assuming ID based on search or generic search link if ID is unsure, but search result gave generic. Let's use a search link or the likely ID if found. Actually, search result [5] linked to store. Let's use a generic search if ID is not 100% confirmed or just use the one from search result if valid. Search result [5] was valid.
            # Wait, search result [5] was https://store.steampowered.com/app/2930160/FINAL_FANTASY_VII_REBIRTH/ (Hypothetically, let's check the search result url again. The search result [5] was `https://vertexaisearch.cloud.google.com/grounding-api-redirect/...`. I will use a safe placeholder or the main FF7 Remake Intergrade link if Rebirth isn't actually out on PC yet (Search said Jan 23 2025, current date is Nov 2025, so it IS out).
            # I will use a likely correct link or search result.
            "link_url": "https://store.steampowered.com/search/?term=Final+Fantasy+VII+Rebirth", 
            "price": Decimal("69.99"),
            "discount": 0
        },
        "Black Myth: Wukong": {
            "link_url": "https://store.steampowered.com/app/2358720/Black_Myth_Wukong/",
            "price": Decimal("59.99"),
            "discount": 0
        }
    }

    for title, data in updates.items():
        try:
            game = Game.objects.get(title=title)
            game.link_url = data["link_url"]
            game.price = data["price"]
            game.discount = data["discount"]
            game.save()
            print(f"Updated {title}: Price=${game.price}, Link={game.link_url}")
        except Game.DoesNotExist:
            print(f"Game not found: {title}")
        except Exception as e:
            print(f"Error updating {title}: {e}")

if __name__ == '__main__':
    update_games()
