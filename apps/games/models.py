from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(help_text="URL de la imagen del juego")
    link_url = models.URLField(help_text="Enlace al juego o tienda")
    genre = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    release_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
