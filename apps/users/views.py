from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    '''Página principal'''
    context = {
        'title': 'GG Rewards - Inicio'
    }
    return render(request, 'home.html', context)

@login_required
def profile(request):
    '''Perfil del usuario'''
    context = {
        'title': 'Mi Perfil',
        'user': request.user
    }
    return render(request, 'users/profile.html', context)
