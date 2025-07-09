from decimal import Decimal
from django.db import models
import cloudinary.uploader
from cloudinary.uploader import upload
from cloudinary.models import CloudinaryField
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
    image_principal = CloudinaryField('image', blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    gearbox = models.CharField(max_length=10, choices=GEARBOX_CHOICES)
    location = models.CharField(max_length=10, choices=LOCATION_CHOICES)
    color = models.CharField(max_length=50)
    air_conditioning = models.BooleanField(default=True)
    discount_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.model

    def get_discounted_price(self):
        if self.discount_active and self.discount_percentage > 0:
            discount_factor = Decimal('1.0') - (Decimal(self.discount_percentage) / Decimal('100'))
            return self.price_per_day * discount_factor
        return self.price_per_day

    def save(self, *args, **kwargs):
        # Se è presente un'immagine locale da caricare
        if self.image_principal and not self.pk:
            upload_result = upload(
                self.image_principal,
                folder=f'cars/{self.model}',
                transformation={"width": 750, "height": 500, "crop": "fill"}
            )
            self.image_principal = upload_result['public_id']  # salva solo l'ID pubblico
        super().save(*args, **kwargs)


class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='gallery', on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.car.model}"



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
        try:
            cloudinary.uploader.destroy(old_image.public_id)
        except Exception as e:
            print(f"Errore eliminazione immagine Cloudinary: {e}")

# Elimina le immagini secondarie quando vengono cancellate (dal formset o dalla cascata)
@receiver(pre_delete, sender=CarImage)
def delete_secondary_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        try:
            cloudinary.uploader.destroy(instance.image.public_id)
        except Exception as e:
            print(f"Errore eliminazione immagine secondaria Cloudinary: {e}")
