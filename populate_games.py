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
            "image_url": "https://cdn1.epicgames.com/offer/77f2b98e2cef40c8a7437518bf420e47/EGS_Cyberpunk2077_CDPROJEKTRED_S2_03_1200x1600-b1847981214ac013383111fc457eb9c5",
            "link_url": "https://www.cyberpunk.net/",
            "genre": "RPG",
            "rating": 4.8,
            "release_date": date(2020, 12, 10)
        },
        {
            "title": "Hollow Knight: Silksong",
            "description": "¡Descubre un vasto reino embrujado en Hollow Knight: Silksong! La secuela de la galardonada aventura de acción.",
            "image_url": "https://i.redd.it/d15xkfw5qqg21.png",
            "link_url": "https://hollowknightsilksong.com/",
            "genre": "Metroidvania",
            "rating": 4.9,
            "release_date": date(2024, 1, 1)
        },
        {
            "title": "Elden Ring",
            "description": "Levántate, Sinluz, y déjate guiar por la gracia para esgrimir el poder del Anillo de Elden y convertirte en un Señor de Elden en las Tierras Intermedias.",
            "image_url": "https://image.api.playstation.com/vulcan/ap/rnd/202110/2000/aGhopp3MHppi7kooGE2Dtt8C.png",
            "link_url": "https://en.bandainamcoent.eu/elden-ring/elden-ring",
            "genre": "RPG de Acción",
            "rating": 4.9,
            "release_date": date(2022, 2, 25)
        },
        {
            "title": "God of War Ragnarök",
            "description": "Kratos y Atreus deben viajar a cada uno de los Nueve Reinos en busca de respuestas mientras las fuerzas asgardianas se preparan para la batalla profetizada que acabará con el mundo.",
            "image_url": "https://image.api.playstation.com/vulcan/ap/rnd/202207/1210/4xJ8XB3bi888QTLZYdl7Oi0s.png",
            "link_url": "https://www.playstation.com/es-es/games/god-of-war-ragnarok/",
            "genre": "Acción y Aventura",
            "rating": 4.9,
            "release_date": date(2022, 11, 9)
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
