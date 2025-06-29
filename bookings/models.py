from django.db import models
from cars.models import Car
from django.conf import settings
from decimal import Decimal

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcola i giorni di prenotazione (inclusivo)
        num_days = (self.end_date - self.start_date).days + 1
        self.total_price = Decimal(num_days) * self.car.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.car.model} ({self.start_date} to {self.end_date})"
