from django.contrib import admin
from .models import Car, CarImage, Category

# Register your models here.

admin.site.register(Category)
admin.site.register(CarImage)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'category', 'price_per_day', 'discount_active', 'discount_percentage')
    list_editable = ('discount_active', 'discount_percentage')