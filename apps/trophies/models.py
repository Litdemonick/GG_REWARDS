from django.db import models
from django.contrib.auth.models import User

class Platform(models.Model):
    '''Plataformas de videojuegos'''
    PLATFORM_CHOICES = [
        ('steam', 'Steam'),
        ('playstation', 'PlayStation'),
        ('xbox', 'Xbox'),
        ('nintendo', 'Nintendo Switch'),
    ]
    
    name = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    icon = models.ImageField(upload_to='platforms/', blank=True, null=True)
    
    class Meta:
        db_table = 'platforms'
        verbose_name = 'Plataforma'
        verbose_name_plural = 'Plataformas'
    
    def __str__(self):
        return self.get_name_display()


class Game(models.Model):
    '''Videojuegos'''
    name = models.CharField(max_length=200)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='games')
    external_id = models.CharField(max_length=100)
    cover_image = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'games'
        verbose_name = 'Videojuego'
        verbose_name_plural = 'Videojuegos'
        unique_together = ['external_id', 'platform']
    
    def __str__(self):
        return f'{self.name} ({self.platform})'


class Trophy(models.Model):
    '''Trofeos/Logros de los juegos'''
    RARITY_CHOICES = [
        ('bronze', 'Bronce'),
        ('silver', 'Plata'),
        ('gold', 'Oro'),
        ('platinum', 'Platino'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='trophies')
    name = models.CharField(max_length=200)
    description = models.TextField()
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    points = models.IntegerField(default=0)
    icon = models.URLField(blank=True, null=True)
    external_id = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'trophies'
        verbose_name = 'Trofeo'
        verbose_name_plural = 'Trofeos'
        unique_together = ['external_id', 'game']
    
    def __str__(self):
        return f'{self.name} - {self.game.name}'


class UserTrophy(models.Model):
    '''Relación entre usuarios y trofeos desbloqueados'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_trophies')
    trophy = models.ForeignKey(Trophy, on_delete=models.CASCADE, related_name='users_unlocked')
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_trophies'
        verbose_name = 'Trofeo de Usuario'
        verbose_name_plural = 'Trofeos de Usuarios'
        unique_together = ['user', 'trophy']
    
    def __str__(self):
        return f'{self.user.username} - {self.trophy.name}'
