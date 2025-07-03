from django.db.models.signals import post_delete
from pages.models import Team
from django.dispatch import receiver
from django.db.models.signals import pre_save
import os

@receiver(post_delete, sender=Team)
def delete_team_photo_on_delete(sender, instance, **kwargs):
    if instance.photo and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)

@receiver(pre_save, sender=Team)
def delete_old_photo_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # nuovo oggetto, nessuna immagine precedente

    try:
        old_photo = Team.objects.get(pk=instance.pk).photo
    except Team.DoesNotExist:
        return

    new_photo = instance.photo
    if old_photo and old_photo != new_photo:
        if old_photo.path and os.path.isfile(old_photo.path):
            os.remove(old_photo.path)