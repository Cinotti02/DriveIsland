from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload
from django.db import models

class Team(models.Model):
     first_name = models.CharField(max_length=255)
     last_name = models.CharField(max_length=255)
     designation = models.CharField(max_length=255)
     photo = CloudinaryField('image', blank=True, null=True)
     facebook_link = models.URLField(max_length=255)
     twitter_link = models.URLField(max_length=255)
     google_link = models.URLField(max_length=255)
     created_date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.first_name

     def save(self, *args, **kwargs):
          # Se è una nuova immagine (non già su Cloudinary)
          if self.photo and not self.pk:
               upload_result = upload(
                    self.photo,
                    folder='team/',
                    transformation={
                         'width': 500,
                         'height': 500,
                         'crop': 'fill',
                         'gravity': 'auto'
                    }
               )
               self.photo = upload_result['public_id']  # salva solo l'id Cloudinary

          super().save(*args, **kwargs)