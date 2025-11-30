from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # El archivo se subirá a MEDIA_ROOT/avatars/user_<id>/<filename>
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='avatars/default.png')
    steam_id = models.CharField(max_length=17, blank=True, null=True)
    xp = models.IntegerField(default=0)
    trophies = models.IntegerField(default=0)
    games_cache = models.JSONField(default=list, blank=True)
    rank = models.CharField(max_length=50, default='Novato')
    level = models.IntegerField(default=1)

    def calculate_rank(self):
        """Devuelve el nombre del rango basado en el nivel del usuario"""
        if self.level < 5: return "Novato"
        if self.level < 10: return "Aprendiz"
        if self.level < 20: return "Profesional"
        if self.level < 50: return "Veterano"
        if self.level < 100: return "Maestro"
        return "Leyenda"

    def save(self, *args, **kwargs):
        # Recalcular rango antes de guardar
        self.rank = self.calculate_rank()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Perfil de {self.user.username}'