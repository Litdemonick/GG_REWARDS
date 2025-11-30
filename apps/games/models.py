from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(help_text="URL de la imagen del juego")
    link_url = models.URLField(help_text="Enlace al juego o tienda")
    genre = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    release_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.IntegerField(default=0, help_text="Porcentaje de descuento (0-100)")
    
    @property
    def discounted_price(self):
        if self.discount > 0:
            from decimal import Decimal
            return round(self.price * (Decimal(1) - Decimal(self.discount) / Decimal(100)), 2)
        return self.price

    def __str__(self):
        return self.title
