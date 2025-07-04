from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'start_date', 'end_date', 'created_at')
    list_filter = ('start_date', 'end_date', 'car')
    search_fields = ('user__username', 'car__model')