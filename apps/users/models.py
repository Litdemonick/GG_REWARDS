from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # El archivo se subirá a MEDIA_ROOT/avatars/user_<id>/<filename>
    return f'avatars/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_directory_path, default='avatars/default.png')
    steam_id = models.CharField(max_length=17, blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'