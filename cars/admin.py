from django.contrib import admin
from .models import Car, CarImage, Booking, Category

# Register your models here.

admin.site.register(Category)
admin.site.register(Car)
admin.site.register(CarImage)
admin.site.register(Booking)