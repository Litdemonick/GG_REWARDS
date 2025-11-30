import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gg_rewards.settings')
django.setup()

from apps.games.models import Game

def populate_games():
    games_data = [
        # Acción / RPG
        {"title": "Black Myth: Wukong", "price": 59.99, "discount": 0, "genre": "Acción", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/2358720/header.jpg"},
        {"title": "Elden Ring", "price": 47.99, "discount": 0, "genre": "RPG", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg"},
        {"title": "Cyberpunk 2077", "price": 44.99, "discount": 65, "genre": "RPG", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1091500/header.jpg"},
        {"title": "God of War Ragnarök", "price": 49.99, "discount": 20, "genre": "Acción", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/2322010/header.jpg"},
        {"title": "Final Fantasy VII Rebirth", "price": 54.99, "discount": 50, "genre": "RPG", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1462040/header.jpg"},
        {"title": "Hollow Knight: Silksong", "price": 6.99, "discount": 0, "genre": "Metroidvania", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1030300/header.jpg"},
        {"title": "Baldur's Gate 3", "price": 34.99, "discount": 0, "genre": "RPG", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1086940/header.jpg"},
        
        # FPS / Shooter
        {"title": "Call of Duty: Black Ops 6", "price": 69.99, "discount": 0, "genre": "Shooter", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/2933620/header.jpg"},
        {"title": "Warhammer 40,000: Space Marine 2", "price": 59.99, "discount": 0, "genre": "Shooter", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/2183900/header.jpg"},
        {"title": "S.T.A.L.K.E.R. 2", "price": 59.99, "discount": 0, "genre": "Shooter", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1643320/header.jpg"},
        
        # Estrategia / Simulación
        {"title": "Civilization VII", "price": 69.99, "discount": 0, "genre": "Estrategia", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1295660/header.jpg"},
        {"title": "Frostpunk 2", "price": 44.99, "discount": 10, "genre": "Estrategia", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1601580/header.jpg"},
        {"title": "Manor Lords", "price": 39.99, "discount": 25, "genre": "Estrategia", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1363080/header.jpg"},
        
        # Indie / Otros
        {"title": "Hades II", "price": 29.99, "discount": 0, "genre": "Roguelike", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1145350/header.jpg"},
        {"title": "The Plucky Squire", "price": 29.99, "discount": 0, "genre": "Aventura", "image": "https://cdn.cloudflare.steamstatic.com/steam/apps/1627570/header.jpg"},
    ]

    for game_data in games_data:
        game, created = Game.objects.update_or_create(
            title=game_data["title"],
            defaults={
                "price": game_data["price"],
                "discount": game_data["discount"],
                "genre": game_data["genre"],
                "image_url": game_data["image"],
                "description": f"Juego épico de {game_data['genre']}"
            }
        )
        if created:
            print(f"Creado: {game.title}")
        else:
            print(f"Actualizado: {game.title} - ${game.price} (-{game.discount}%)")

if __name__ == '__main__':
    populate_games()
