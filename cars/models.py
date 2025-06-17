from django.db import models

from django.utils.text import slugify

# Create your models here.

def car_image_upload_to(instance, filename):
    model_slug = slugify(instance.model)
    return f"cars/{model_slug}/{filename}"


def car_secondary_image_upload_to(instance, filename):
    model_slug = slugify(instance.car.model)
    return f"cars/{model_slug}/secondary/{filename}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Car(models.Model):
    FUEL_CHOICES = [
        ('Diesel', 'Diesel'),
        ('Benzina', 'Benzina'),
        ('Elettrico', 'Elettrico'),
        ('Ibrido', 'Ibrido'),
    ]

    GEARBOX_CHOICES = [
        ('Manuale', 'Manuale'),
        ('Automatico', 'Automatico'),
    ]
    LOCATION_CHOICES = [
        ('Aeroporto', 'Aeroporto'),
        ('Ufficio', 'Ufficio'),
        ('Port', 'Porto'),
    ]
    category = models.ForeignKey(Category, related_name='cars', on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    image_principal = models.ImageField(upload_to=car_image_upload_to)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    gearbox = models.CharField(max_length=10, choices=GEARBOX_CHOICES)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    air_conditioning = models.BooleanField(default=True)
    color = models.CharField(max_length=50)


    def __str__(self):
        return self.model


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=car_secondary_image_upload_to)

    def __str__(self):
        return f"Image for {self.car.model}"


class Booking(models.Model):
    car = models.ForeignKey(Car, related_name='bookings', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.car.model} ({self.start_date} → {self.end_date})"
