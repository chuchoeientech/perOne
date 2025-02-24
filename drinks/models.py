from django.db import models
import uuid


class DrinkSession(models.Model):
    session_id = models.UUIDField(
        unique=True, editable=False, default=uuid.uuid4)
    timestamp = models.DateTimeField(auto_now_add=True)
    beer_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.session_id:  # Si no tiene un session_id, generar uno
            self.session_id = uuid.uuid4()
        super().save(*args, **kwargs)

    def total_price(self, beer_price):
        return self.beer_count * beer_price

    def total_price_with_tip(self, beer_price):
        propina = self.total_price(beer_price) * 0.10
        return self.total_price(beer_price) + propina

    def __str__(self):
        return f"Session {self.session_id} - {self.beer_count} beers"
