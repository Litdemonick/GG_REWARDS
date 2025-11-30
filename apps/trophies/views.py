from django.shortcuts import render
from apps.games.models import Game

def game_catalog(request):
    games = Game.objects.all()
    context = {
        'title': 'Catálogo de Juegos',
        'games': games
    }
    return render(request, 'trophies/game_catalog.html', context)