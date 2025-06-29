from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Aggiunge classe CSS e placeholder a tutti i campi
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email'
        })
        self.fields['subject'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Subject'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Phone Number'
        })
        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Write your message'
        })

        # Se l'utente è loggato: precompila e blocca
        if user and getattr(user, 'is_authenticated', False):
            full_name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
            self.fields['name'].initial = full_name or getattr(user, 'username', '')
            self.fields['email'].initial = getattr(user, 'email', '')
            self.fields['phone'].initial = getattr(user, 'phone_number', '')

            self.fields['name'].disabled = True
            self.fields['email'].disabled = True
            self.fields['phone'].disabled = True

    def clean_message(self):
        data = self.cleaned_data['message']
        if len(data.strip()) < 10:
            raise forms.ValidationError("Il messaggio è troppo breve.")
        return data