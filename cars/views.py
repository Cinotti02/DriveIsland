from django.shortcuts import render, redirect
from .forms import CarForm
from .models import Car, Category
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.db.models import Exists, OuterRef
from bookings.models import Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test


def cars_list(request):
    car = Car.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(car, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    is_admin = request.user.is_authenticated and request.user.groups.filter(name="Amministratore").exists()

    return render(request, 'pages/../cars/cars.html', {
        'page_obj': page_obj,
        'categories': categories,
        'cars': car,
        'models': Car.objects.values_list('model', flat=True).distinct(),
        'locations': dict(Car.LOCATION_CHOICES),
        'gearboxes': dict(Car.GEARBOX_CHOICES),
        'is_admin': is_admin,
    })

def car_search(request):
    car = Car.objects.all()

    if request.GET.get('category'):
        car = car.filter(category__name__icontains=request.GET['category'])
    if request.GET.get('model'):
        car = car.filter(model__icontains=request.GET['model'])
    if request.GET.get('fuel_type'):
        car = car.filter(fuel_type=request.GET['fuel_type'])
    if request.GET.get('gearbox'):
        car = car.filter(gearbox=request.GET['gearbox'])
    if request.GET.get('location'):
        car = car.filter(location=request.GET['location'])
    if request.GET.get('color'):
        car = car.filter(color__iexact=request.GET['color'])
    if request.GET.get('air_conditioning') in ['true', 'false']:
        car = car.filter(air_conditioning=(request.GET['air_conditioning'] == 'true'))
    if request.GET.get('min_price'):
        car = car.filter(price_per_day__gte=request.GET['min_price'])
    if request.GET.get('max_price'):
        car = car.filter(price_per_day__lte=request.GET['max_price'])

    # Filtro per date
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            today = date.today()

            if start > end:
                messages.warning(request, "La data di inizio non può essere dopo la data di fine.")
                car = Car.objects.none()
            elif start < today:
                messages.warning(request, "La data di inizio non può essere nel passato.")
                car = Car.objects.none()
            else:
                print("Filtro attivo: da", start, "a", end)
                print("Auto iniziali:", car.count())
                conflicting_bookings = Booking.objects.filter(
                    car=OuterRef('pk'),
                    start_date__lte=end,
                    end_date__gte=start
                )

                car = car.annotate(
                    has_conflict=Exists(conflicting_bookings)
                ).filter(has_conflict=False)

        except ValueError:
            messages.warning(request, "Formato data non valido.")
            car = Car.objects.none()


    context = {
            'cars': car,
            'categories': Category.objects.all(),
            'models': Car.objects.values_list('model', flat=True).distinct(),
            'colors': Car.objects.values_list('color', flat=True).distinct(),
            'fuel_types': dict(Car.FUEL_CHOICES),
            'gearboxes': dict(Car.GEARBOX_CHOICES),
            'locations': dict(Car.LOCATION_CHOICES),
        }

    return render(request, 'cars/search.html', context)

def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    is_admin = request.user.is_authenticated and request.user.groups.filter(name="Amministratore").exists()
    return render(request, 'cars/car_details.html', {
        'car': car,
        'categories': Category.objects.all(),
        'models': Car.objects.values_list('model', flat=True).distinct(),
        'locations': dict(Car.LOCATION_CHOICES),
        'gearboxes': dict(Car.GEARBOX_CHOICES),
        'is_admin': is_admin,
    })

def is_group_admin(user):
    return user.groups.filter(name="Amministratore").exists()

@login_required
@user_passes_test(is_group_admin)
def car_edit(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "Modifiche salvate con successo ✅")
            return redirect('car_details', car_id=car.pk)
        else:
            messages.error(request, "Correggi gli errori nel modulo.")
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/car_edit.html', {
        'form': form,
        'car': car,
        'title': f"Modifica {car.model}",
    })