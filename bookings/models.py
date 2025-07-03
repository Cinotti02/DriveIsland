from django.db import models
from cars.models import Car
from django.conf import settings
from decimal import Decimal
from datetime import time, timedelta, datetime
from django.utils.timezone import make_aware, is_naive, get_current_timezone


class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(default="10:00")
    end_time = models.TimeField(default="10:00")
    pickup_location = models.CharField(max_length=100, default="Ufficio")
    return_location = models.CharField(max_length=100, default="Ufficio")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):

        # Calcola il prezzo totale basato sui giorni di prenotazione e sul prezzo giornaliero dell'auto
        num_days = (self.end_date - self.start_date).days + 1
        daily_price = self.car.price_per_day

        # Applica lo sconto se attivo
        if self.car.discount_active and self.car.discount_percentage:
            discount = (Decimal(self.car.discount_percentage) / Decimal(100)) * daily_price
            daily_price -= discount

        self.total_price = Decimal(num_days) * daily_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.car.model} ({self.start_date} to {self.end_date})"


    @property
    def start_datetime(self):
        dt = datetime.combine(self.start_date, self.start_time)
        if is_naive(dt):
            return make_aware(dt, timezone=get_current_timezone())
        return dt

    @property
    def end_datetime(self):
        dt = datetime.combine(self.end_date, self.end_time)
        if is_naive(dt):
            return make_aware(dt, timezone=get_current_timezone())

def half_hour_choices():
    choices = []
    current = datetime.combine(datetime.today(), time(0, 0))
    for _ in range(48):  # 48 intervalli di mezz'ora in 24h
        choices.append((current.time().strftime('%H:%M'), current.time().strftime('%H:%M')))
        current += timedelta(minutes=30)
    return choices
