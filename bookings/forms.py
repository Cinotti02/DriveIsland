from django import forms
from .models import Booking, Car, half_hour_choices
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

RETURN_LOCATIONS = [
    ('Ufficio', 'Ufficio'),
    ('Aeroporto', 'Aeroporto'),
    ('Porto', 'Porto'),
]


class BookingForm(forms.ModelForm):
    start_time = forms.ChoiceField(choices=half_hour_choices(), label="Ora ritiro")
    end_time = forms.ChoiceField(choices=half_hour_choices(), label="Ora riconsegna")
    return_location = forms.ChoiceField(choices=RETURN_LOCATIONS)

    class Meta:
        model = Booking
        fields = ['car', 'start_date', 'start_time', 'end_date', 'end_time', 'pickup_location', 'return_location',
                  'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'step': 1800}),  # step 1800s = 30min
            'end_time': forms.TimeInput(attrs={'type': 'time', 'step': 1800}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        car = cleaned_data.get('car')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date == end_date and start_time and end_time:
            if end_time <= start_time:
                raise ValidationError("⏰ L'orario di riconsegna deve essere successivo a quello di ritiro.")

        if start_date and end_date and car:
            overlapping_bookings = Booking.objects.filter(
                car=car,
                start_date__lte=end_date,
                end_date__gte=start_date,
            )
            if overlapping_bookings.exists():
                raise ValidationError("❌ La macchina è già prenotata in queste date.")


User = get_user_model()


class BookingFilterForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all(), required=False, label="Auto")
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label="Utente")
    date = forms.DateField(required=False, label="Data", widget=forms.DateInput(attrs={'type': 'date'}))
