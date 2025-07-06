from django.db.models.signals import post_delete, pre_save
from pages.models import Team
from django.dispatch import receiver
import cloudinary.uploader

@receiver(post_delete, sender=Team)
def delete_team_photo_on_delete(sender, instance, **kwargs):
    if instance.photo:
        try:
            cloudinary.uploader.destroy(instance.photo.public_id)
        except Exception as e:
            print(f"Errore nell'eliminazione della foto Team da Cloudinary: {e}")

@receiver(pre_save, sender=Team)
def delete_old_photo_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # Nuovo oggetto, nessuna immagine precedente da confrontare

    try:
        old_instance = Team.objects.get(pk=instance.pk)
        old_photo = old_instance.photo
    except Team.DoesNotExist:
        return

    new_photo = instance.photo
    if old_photo and old_photo != new_photo:
        try:
            cloudinary.uploader.destroy(old_photo.public_id)
        except Exception as e:
            print(f"Errore nella sostituzione della vecchia immagine Team su Cloudinary: {e}")