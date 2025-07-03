from django import forms
from django.forms import modelformset_factory
from .models import Car, CarImage

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image']  # o altri campi rilevanti

# Un formset per più immagini
CarImageFormSet = modelformset_factory(CarImage, form=CarImageForm, extra=0, can_delete=True)