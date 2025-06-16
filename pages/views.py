from django.shortcuts import render
from django.core.paginator import Paginator
from pages.models import Team
from cars.models import Car


# Create your views here.
def home(request):
    team = Team.objects.all()
    return render(request, 'pages/home.html', {'team': team})

def cars(request):
    car = Car.objects.all()
    paginator = Paginator(car, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/cars.html', {'page_obj': page_obj})

def about(request):
    team = Team.objects.all()
    return render(request, 'pages/about.html', {'team': team})

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    return render(request, 'pages/contact.html')

