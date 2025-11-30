import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game
from datetime import date

def populate_games():
    games_data = [
        {
            "title": "Cyberpunk 2077",
            "description": "Cyberpunk 2077 es una historia de acción y aventura de mundo abierto ambientada en Night City, una megalópolis obsesionada con el poder, el glamour y la modificación corporal.",
            "image_url": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1091500/library_600x900.jpg",
            "link_url": "https://store.steampowered.com/app/1091500/Cyberpunk_2077/",
            "genre": "RPG",
            "rating": 4.8,
            "release_date": date(2020, 12, 10),
            "price": 20.99,
            "discount": 65
        },
        {
            "title": "Hollow Knight: Silksong",
            "description": "¡Descubre un vasto reino embrujado en Hollow Knight: Silksong! La secuela de la galardonada aventura de acción.",
            "image_url": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1030300/library_600x900.jpg",
            "link_url": "https://store.steampowered.com/app/1030300/Hollow_Knight_Silksong/",
            "genre": "Metroidvania",
            "rating": 4.9,
            "release_date": date(2024, 1, 1),
            "price": 19.99,
            "discount": 0
        },
        {
            "title": "Elden Ring",
            "description": "Levántate, Sinluz, y déjate guiar por la gracia para esgrimir el poder del Anillo de Elden y convertirte en un Señor de Elden en las Tierras Intermedias.",
            "image_url": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1245620/library_600x900.jpg",
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
            "image_url": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2322010/library_600x900.jpg",
            "link_url": "https://store.steampowered.com/app/2322010/God_of_War_Ragnark/",
            "genre": "Acción y Aventura",
            "rating": 4.9,
            "release_date": date(2022, 11, 9),
            "price": 47.99,
            "discount": 20
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
            "title": "Final Fantasy VII Rebirth",
            "description": "El viaje hacia lo desconocido continúa. Tras escapar de la ciudad distópica de Midgar, Cloud y sus amigos se embarcan en un viaje a través del planeta.",
            "image_url": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2909400/library_600x900.jpg",
            "link_url": "https://store.steampowered.com/app/2909400/FINAL_FANTASY_VII_REBIRTH/",
            "genre": "RPG",
            "rating": 4.8,
            "release_date": date(2024, 2, 29),
            "price": 69.99,
            "discount": 50
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
        game, created = Game.objects.get_or_create(
            title=game_data["title"],
            defaults=game_data
        )
        if created:
            print(f"Created game: {game.title}")
        else:
            print(f"Game already exists: {game.title}")

if __name__ == '__main__':
    populate_games()
