from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Campi aggiuntivi', {'fields': ('phone_number', 'date_of_birth')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campi aggiuntivi', {'fields': ('phone_number', 'date_of_birth')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)