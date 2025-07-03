from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from .forms import CarForm, CarImageForm
from .models import Car, Category, CarImage
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from datetime import datetime, date
from django.forms import modelformset_factory
from django.db.models import Exists, OuterRef
from bookings.models import Booking
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import F, ExpressionWrapper, DecimalField, Case, When, Value

import logging
logger = logging.getLogger(__name__)

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

    car = car.annotate(
        effective_price=ExpressionWrapper(
            Case(
                When(discount_active=True, discount_percentage__gt=0,
                     then=F('price_per_day') * (1 - F('discount_percentage') / Value(100.0))),
                default=F('price_per_day'),
                output_field=DecimalField()
            ),
            output_field=DecimalField()
        )
    )

    if request.GET.get('min_price'):
        car = car.filter(effective_price__gte=request.GET['min_price'])
    if request.GET.get('max_price'):
        car = car.filter(effective_price__lte=request.GET['max_price'])


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


@user_passes_test(is_group_admin)
def car_edit(request, car_id):
    car = get_object_or_404(Car, pk=car_id)

    image_formset_class = modelformset_factory(CarImage, form=CarImageForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        formset = image_formset_class(request.POST, request.FILES, queryset=CarImage.objects.filter(car=car))
        secondary_images = request.FILES.getlist('secondary_images')

        if form.is_valid() and formset.is_valid():
            form.save()
            logger.info(f"Auto ID {car.id} ({car.model}) modificata da {request.user}")



            # salva immagini secondarie
            for image_form in formset:
                if image_form.cleaned_data.get('DELETE') and image_form.instance.pk:
                    image_form.instance.delete()
                elif image_form.cleaned_data.get('image'):
                    new_img = image_form.save(commit=False)
                    new_img.car = car
                    new_img.save()

            for image_file in secondary_images:
                CarImage.objects.create(car=car, image=image_file)

            messages.success(request, "Auto aggiornata con successo.")
            return redirect('cars')

        else:
            messages.error(request, "Correggi gli errori nel modulo.")
    else:
        form = CarForm(instance=car)
        formset = image_formset_class(queryset=CarImage.objects.filter(car=car))

    return render(request, 'cars/car_edit.html', {
        'form': form,
        'formset': formset,
        'car': car,
        'title': f"Modifica {car.model}",
    })


@user_passes_test(is_group_admin)
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        secondary_images = request.FILES.getlist('secondary_images')

        if form.is_valid():
            car = form.save(commit=False)
            car.image_principal = None
            form.save()

            if 'image_principal' in request.FILES:
                car.image_principal = request.FILES['image_principal']
                car.save()

                for image in secondary_images:
                    CarImage.objects.create(car=car, image=image)

                logger.info(f"Nuova auto aggiunta: {car.model} da parte di {request.user}")
                return redirect('cars')

            else:
                print("Errore nel salvataggio dell'immagine:", form.errors)
        else:
            print("Errore nel primo form:", form.errors)
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})

@login_required
@user_passes_test(is_group_admin)
def delete_car(request, car_id):
    if request.method != 'POST':
        messages.warning(request, "Operazione non consentita.")
        return redirect('car_edit', car_id=car_id)

    car = get_object_or_404(Car, id=car_id)
    future_bookings = car.booking_set.filter(start_date__gt=now())

    for booking in future_bookings:
        user = booking.user
        send_booking_cancellation_email(user, booking, car)
        logger.info(
            f"Prenotazione ID {booking.id} cancellata per auto eliminata ({car.model}) - utente notificato: {user}")
        booking.delete()

    logger.info(f"Auto ID {car.id} ({car.model}) eliminata da {request.user}")
    car.delete()

    messages.success(request, "Auto eliminata con successo.")
    return redirect('cars')

def send_booking_cancellation_email(user, booking, car):
    html_content = render_to_string('cars/booking_cancelled_email.html', {
        'user': user,
        'booking': booking,
        'car': car,
        'site_url': 'https://driveisland.com',
        'current_year': now().year
    })

    subject = "Prenotazione Annullata - DriveIsland"
    msg = EmailMultiAlternatives(
        subject=subject,
        body="Prenotazione annullata.",
        from_email="noreply@driveisland.com",
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

