from django.shortcuts import render
from pages.models import Team
from cars.models import Car, Category


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
