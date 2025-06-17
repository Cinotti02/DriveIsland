from django.shortcuts import render
from .models import Car, Category

def car_search(request):
    cars = Car.objects.all()

    if request.GET.get('category'):
        cars = cars.filter(category__name__icontains=request.GET['category'])
    if request.GET.get('model'):
        cars = cars.filter(model__icontains=request.GET['model'])
    if request.GET.get('fuel_type'):
        cars = cars.filter(fuel_type=request.GET['fuel_type'])
    if request.GET.get('gearbox'):
        cars = cars.filter(gearbox=request.GET['gearbox'])
    if request.GET.get('location'):
        cars = cars.filter(location=request.GET['location'])
    if request.GET.get('color'):
        cars = cars.filter(color__iexact=request.GET['color'])
    if request.GET.get('air_conditioning') in ['true', 'false']:
        cars = cars.filter(air_conditioning=(request.GET['air_conditioning'] == 'true'))
    if request.GET.get('min_price'):
        cars = cars.filter(price_per_day__gte=request.GET['min_price'])
    if request.GET.get('max_price'):
        cars = cars.filter(price_per_day__lte=request.GET['max_price'])

    context = {
        'cars': cars,
        'categories': Category.objects.all(),
        'models': Car.objects.values_list('model', flat=True).distinct(),
        'colors': Car.objects.values_list('color', flat=True).distinct(),
        'fuel_types': dict(Car.FUEL_CHOICES),
        'gearboxes': dict(Car.GEARBOX_CHOICES),
        'locations': dict(Car.LOCATION_CHOICES),
    }

    return render(request, 'cars/search.html', context)