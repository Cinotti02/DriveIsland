from django import forms
from .models import Booking
from django.core.exceptions import ValidationError

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get('car')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and car:
            overlapping_bookings = Booking.objects.filter(
                car=car,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
            if overlapping_bookings.exists():
                raise ValidationError("❌ La macchina è già prenotata in queste date.")