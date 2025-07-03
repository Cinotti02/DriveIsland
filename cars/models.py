from django.db import models
from PIL import Image
import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify


def car_image_upload_to(instance, filename):
    model_slug = slugify(instance.model)
    return f"cars/{model_slug} {instance.id}/{filename}"


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
    image_principal = models.ImageField(upload_to=car_image_upload_to, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    gearbox = models.CharField(max_length=10, choices=GEARBOX_CHOICES)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    air_conditioning = models.BooleanField(default=True)
    color = models.CharField(max_length=50)


    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Percorso assoluto all'immagine salvata
        if self.image_principal:
            img_path = self.image_principal.path
            try:
                img = Image.open(img_path)
                fixed_size = (750, 500)
                img = img.resize(fixed_size)
                img.save(img_path)
            except Exception as e:
                print(f"Errore nel ridimensionamento dell'immagine: {e}")


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=car_secondary_image_upload_to)

    def __str__(self):
        return f"Image for {self.car.model}"

# Elimina l'immagine principale quando l'auto viene cancellata
@receiver(pre_delete, sender=Car)
def delete_main_image_on_car_delete(sender, instance, **kwargs):

    if instance.image_principal and os.path.isfile(instance.image_principal.path):
        try:
            os.remove(instance.image_principal.path)
        except (FileNotFoundError, ValueError):
            pass

    # Prova a eliminare la cartella del modello se vuota
    model_slug = slugify(instance.model)
    model_folder = os.path.join('media', 'cars', model_slug)
    secondary_folder = os.path.join('media', 'cars', model_slug, 'secondary')

    for folder in [secondary_folder, model_folder]:
        if os.path.isdir(folder) and not os.listdir(folder):
            try:
                os.rmdir(folder)
            except OSError:
                pass

# Elimina l'immagine principale se viene sostituita da una nuova
@receiver(pre_save, sender=Car)
def delete_old_main_image_on_update(sender, instance, **kwargs):

    # Nuovo oggetto, nessuna immagine da eliminare
    if not instance.pk:
        return
    try:
        old_instance = Car.objects.get(pk=instance.pk)
    except Car.DoesNotExist:
        return

    old_image = old_instance.image_principal
    new_image = instance.image_principal

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            try:
                os.remove(old_image.path)
            except (FileNotFoundError, ValueError):
                pass

# Elimina le immagini secondarie quando vengono cancellate (dal formset o dalla cascata)
@receiver(pre_delete, sender=CarImage)
def delete_secondary_image_on_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
