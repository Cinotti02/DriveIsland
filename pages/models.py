from django.db import models

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

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    reply = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.email}"