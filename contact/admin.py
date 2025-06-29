from django.contrib import admin

from .models import ContactMessage

# Register your models here.

admin.site.register(ContactMessage, list_display=['subject', 'email', 'created_at'], search_fields=['subject', 'email'], list_filter=['created_at'], ordering=['-created_at'])