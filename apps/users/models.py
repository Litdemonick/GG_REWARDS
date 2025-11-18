from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    '''Perfil extendido del usuario'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    
    # IDs de cuentas en diferentes plataformas
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    psn_id = models.CharField(max_length=100, blank=True, null=True)
    xbox_id = models.CharField(max_length=100, blank=True, null=True)
    nintendo_id = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def calculate_level(self):
        '''Calcula el nivel basado en la experiencia'''
        return (self.experience // 100) + 1
    
    def add_experience(self, amount):
        '''Añade experiencia y actualiza el nivel'''
        self.experience += amount
        self.level = self.calculate_level()
        self.save()
