from django.shortcuts import render
from pages.models import Team
from cars.models import Car, Category

import logging
logger = logging.getLogger(__name__)


def home(request):
    logger.info(f"Homepage visitata da {request.user if request.user.is_authenticated else 'utente anonimo'}")
    team = Team.objects.all()
    cars = Car.objects.all()
    categories = Category.objects.all()
    discounted_cars = Car.objects.filter(discount_active=True)

    latest_cars = Car.objects.order_by('-created_at')[:3]


    return render(request, 'pages/home.html', {
        'team': team,
        'categories': categories,
        'cars': cars,
        'discounted_cars': discounted_cars,
        'models': Car.objects.values_list('model', flat=True).distinct(),
        'locations': dict(Car.LOCATION_CHOICES),
        'gearboxes': dict(Car.GEARBOX_CHOICES),
        'latest_cars': latest_cars,
    })

def about(request):
    team = Team.objects.all()
    return render(request, 'pages/about.html', {
        'team': team
    })

def services(request):
    return render(request, 'pages/services.html')
