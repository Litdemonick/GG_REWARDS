import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game
from datetime import date

def populate_games():
    # Delete Zelda if it exists
    Game.objects.filter(title__icontains="Zelda").delete()
    # Delete Final Fantasy if it exists
    Game.objects.filter(title__icontains="Final Fantasy").delete()
    print("Deleted 'The Legend of Zelda' and 'Final Fantasy' if they existed.")

    games_data = [
        {
            "title": "Cyberpunk 2077",
            "description": "Cyberpunk 2077 es una historia de acción y aventura de mundo abierto ambientada en Night City, una megalópolis obsesionada con el poder, el glamour y la modificación corporal.",
            "image_url": "https://cdn1.epicgames.com/offer/77f2b98e2cef40c8a7437518bf420e47/EGS_Cyberpunk2077_CDPROJEKTRED_S2_03_1200x1600-b1847981214ac013383111fc457eb9c5",
            "link_url": "https://store.steampowered.com/app/1091500/Cyberpunk_2077/",
            "genre": "RPG",
            "rating": 4.8,
            "release_date": date(2020, 12, 10),
            "price": 44.99,
            "discount": 65
        },
        {
            "title": "Hollow Knight: Silksong",
            "description": "¡Descubre un vasto reino embrujado en Hollow Knight: Silksong! La secuela de la galardonada aventura de acción.",
            "image_url": "https://i.redd.it/d15xkfw5qqg21.png",
            "link_url": "https://store.steampowered.com/app/1030300/Hollow_Knight_Silksong/",
            "genre": "Metroidvania",
            "rating": 4.9,
            "release_date": date(2024, 1, 1),
            "price": 6.99,
            "discount": 0
        },
        {
            "title": "Elden Ring",
            "description": "Levántate, Sinluz, y déjate guiar por la gracia para esgrimir el poder del Anillo de Elden y convertirte en un Señor de Elden en las Tierras Intermedias.",
            "image_url": "https://image.api.playstation.com/vulcan/ap/rnd/202110/2000/aGhopp3MHppi7kooGE2Dtt8C.png",
            "link_url": "https://store.steampowered.com/app/1245620/ELDEN_RING/",
            "genre": "RPG de Acción",
            "rating": 4.9,
            "release_date": date(2022, 2, 25),
            "price": 59.99,
            "discount": 0
        },
        {
            "title": "God of War Ragnarök",
            "description": "Kratos y Atreus deben viajar a cada uno de los Nueve Reinos en busca de respuestas mientras las fuerzas asgardianas se preparan para la batalla profetizada que acabará con el mundo.",
            "image_url": "https://image.api.playstation.com/vulcan/ap/rnd/202207/1210/4xJ8XB3bi888QTLZYdl7Oi0s.png",
            "link_url": "https://store.steampowered.com/app/2322010/God_of_War_Ragnarok/",
            "genre": "Acción y Aventura",
            "rating": 4.9,
            "release_date": date(2022, 11, 9),
            "price": 49.99,
            "discount": 0
        },
        {
            "title": "Baldur's Gate 3",
            "description": "Reúne a tu grupo y regresa a los Reinos Olvidados en una historia de compañerismo y traición, sacrificio y supervivencia, y la atracción del poder absoluto.",
            "image_url": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1086940/library_600x900.jpg",
            "link_url": "https://store.steampowered.com/app/1086940/Baldurs_Gate_3/",
            "genre": "RPG",
            "rating": 4.9,
            "release_date": date(2023, 8, 3),
            "price": 34.99,
            "discount": 0
        },
        {
            "title": "Black Myth: Wukong",
            "description": "Black Myth: Wukong es un juego de rol de acción basado en la mitología china. La historia se basa en Viaje al Oeste, una de las Cuatro Grandes Novelas Clásicas de la literatura china.",
            "image_url": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2358720/library_600x900.jpg",
            "link_url": "https://store.steampowered.com/app/2358720/Black_Myth_Wukong/",
            "genre": "RPG de Acción",
            "rating": 4.7,
            "release_date": date(2024, 8, 20),
            "price": 59.99,
            "discount": 0
        }
    ]

    for game_data in games_data:
        game, created = Game.objects.update_or_create(
            title=game_data["title"],
            defaults=game_data
        )
        if created:
            print(f"Created game: {game.title}")
        else:
            print(f"Game already exists: {game.title}")

if __name__ == '__main__':
    populate_games()
