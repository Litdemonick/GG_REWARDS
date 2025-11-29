from django.shortcuts import render
from .models import Game
from apps.users.models import Profile
from django.db.models import Count

def game_list(request):
    # 1. Filtrado Básico, Búsqueda y Ordenamiento
    genre_filters = request.GET.getlist('genre') # Obtener lista de géneros
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort')
    only_discounts = request.GET.get('discount')
    
    games = Game.objects.all()

    if search_query:
        games = games.filter(title__icontains=search_query)
    
    if genre_filters:
        # Usar Q objects para buscar si el género del juego CONTIENE alguno de los seleccionados
        # Esto permite que "RPG de Acción" aparezca si seleccionas "RPG" o "Acción"
        from django.db.models import Q
        query = Q()
        for genre in genre_filters:
            query |= Q(genre__icontains=genre)
        games = games.filter(query)

    if only_discounts == 'true':
        games = games.filter(discount__gt=0)

    if sort_by == 'price_asc':
        games = games.order_by('price')
    elif sort_by == 'price_desc':
        games = games.order_by('-price')

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
        'active_filters': genre_filters,
        'search_query': search_query,
        'sort_by': sort_by,
        'only_discounts': only_discounts
    }
    return render(request, 'games/games.html', context)
