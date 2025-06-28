from django.shortcuts import render
from pages.models import Team
from cars.models import Car, Category
from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
def home(request):
    team = Team.objects.all()
    cars = Car.objects.all()
    categories = Category.objects.all()
    return render(request, 'pages/home.html', {
        'team': team,
        'categories': categories,
        'cars': cars,
        'models': Car.objects.values_list('model', flat=True).distinct(),
        'locations': dict(Car.LOCATION_CHOICES),
        'gearboxes': dict(Car.GEARBOX_CHOICES),
    })

def about(request):
    team = Team.objects.all()
    return render(request, 'pages/about.html', {
        'team': team
    })

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    initial = {}
    first_name = getattr(request.user, 'first_name', '')
    last_name = getattr(request.user, 'last_name', '')
    full_name = f'{first_name} {last_name}'.strip() or getattr(request.user, 'username', '')
    initial = {
        'name': full_name,
        'email': getattr(request.user, 'email', ''),
        'phone': getattr(request.user, 'phone_number', '')
        }

    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            if request.user.is_authenticated:
                message.user = request.user  # solo se hai collegato l'utente nel modello
            message.save()
            messages.success(request, "Il tuo messaggio è stato inviato con successo!")
            return redirect('contact')
    else:
        form = ContactForm(initial=initial, user=request.user)

    return render(request, 'pages/contact.html', {'form': form})