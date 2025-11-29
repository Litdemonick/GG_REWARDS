from django.shortcuts import render
from .models import Game
from apps.users.models import Profile
from django.db.models import Count

def game_list(request):
    # 1. Filtrado Básico
    genre_filter = request.GET.get('genre')
    
    if genre_filter:
        games = Game.objects.filter(genre__iexact=genre_filter)
    else:
        games = Game.objects.all()

    # 2. Sistema de Recomendaciones
    recommended_games = []
    
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            steam_games = profile.games_cache
            
            if steam_games:
                # A. Extraemos nombres de juegos que el usuario ha jugado en Steam
                # (Asumiendo que steam_games es una lista de dicts con 'name')
                steam_game_names = [g.get('name') for g in steam_games if g.get('name')]
                
                # B. Buscamos cuáles de esos juegos existen en nuestra DB local
                # para saber qué géneros le gustan al usuario.
                user_known_games = Game.objects.filter(title__in=steam_game_names)
                
                if user_known_games.exists():
                    # C. Encontramos el género más frecuente
                    # values_list devuelve tuplas ('RPG',), ('Action',), etc.
                    favorite_genres = user_known_games.values_list('genre', flat=True)
                    
                    # Contamos manual o con Counter (o con anotaciones si fuera query compleja)
                    from collections import Counter
                    if favorite_genres:
                        genre_counts = Counter(favorite_genres)
                        top_genre = genre_counts.most_common(1)[0][0]
                        
                        # D. Recomendamos juegos de ese género que NO estén en la lista principal (opcional)
                        # o simplemente destacamos juegos de ese género.
                        # Excluimos los que ya jugó (user_known_games) para que descubra nuevos.
                        recommended_games = Game.objects.filter(genre=top_genre).exclude(id__in=user_known_games.values('id'))[:4]

        except Profile.DoesNotExist:
            pass

    context = {
        'games': games,
        'recommended_games': recommended_games,
        'active_filter': genre_filter
    }
    return render(request, 'games/games.html', context)
