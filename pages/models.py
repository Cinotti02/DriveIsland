from django.db import models
from PIL import Image

class Team(models.Model):
     first_name = models.CharField(max_length=255)
     last_name = models.CharField(max_length=255)
     designation = models.CharField(max_length=255)
     photo = models.ImageField(upload_to='team/')
     facebook_link = models.URLField(max_length=255)
     twitter_link = models.URLField(max_length=255)
     google_link = models.URLField(max_length=255)
     created_date = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.first_name

     def save(self, *args, **kwargs):
          super().save(*args, **kwargs)

          # Percorso assoluto all'immagine salvata
          if self.photo:
               img_path = self.photo.path
               try:
                    img = Image.open(img_path)
                    fixed_size = (800,800)
                    img = img.resize(fixed_size)
                    img.save(img_path)
               except Exception as e:
                    print(f"Errore nel ridimensionamento dell'immagine: {e}")