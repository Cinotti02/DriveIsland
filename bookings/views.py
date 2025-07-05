import stripe
from datetime import timedelta
from cars.models import Car
from contact.views import is_admin
from .models import Booking
from .forms import BookingForm, BookingFilterForm
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.core.mail import EmailMultiAlternatives
from django.template import Template, Context
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic.edit import CreateView
from django.views.decorators.http import require_GET

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

import logging
logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'

    def get_initial(self):
        initial = super().get_initial()
        get = self.request.GET

        if get.get('start_date'):
            initial['start_date'] = get['start_date']
        if get.get('end_date'):
            initial['end_date'] = get['end_date']
        if get.get('car'):
            car_id = get.get('car')
            car = Car.objects.filter(id=car_id).first()
            if car:
                initial['pickup_location'] = car.location
            try:
                car_obj = Car.objects.get(id=get['car'])
                initial['pickup_location'] = car_obj.location
            except Car.DoesNotExist:
                pass

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car_id = self.request.GET.get('car') or self.get_initial().get('car')
        context['car'] = Car.objects.filter(id=car_id).first()  # evita errore se non trovato
        return context

    def get_success_url(self):
        return reverse_lazy('booking_success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.request.session['last_booking_id'] = self.object.id
        logger.info(f'Prenotazione creata: ID {self.object.id} da {self.request.user}')
        return redirect('checkout', booking_id=self.object.id)


@login_required
def booking_success(request):
    booking_id = request.session.pop('last_booking_id', None)
    if not booking_id:
        return redirect('dashboard')  # fallback se si accede direttamente

    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'bookings/success.html', {'booking': booking})


@login_required
def start_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "eur",
                "unit_amount": int(booking.total_price * 100),  # in centesimi
                "product_data": {
                    "name": f"Noleggio: {booking.car.model}",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=request.build_absolute_uri(
            reverse("payment_success", args=[booking.id])
        ),
        cancel_url=request.build_absolute_uri(
            reverse("payment_cancel")
        ),
    )

    return redirect(session.url, code=303)

@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.is_paid = True
    booking.payment_date = timezone.now()
    booking.payment_method = "stripe"
    booking.save()

    # Invia email di conferma
    context = {
        'booking': booking,
        'current_year': timezone.now().year,
        'dashboard_url': f"https://{settings.SITE_DOMAIN}{reverse('dashboard')}",
    }
    html_content = render_to_string('bookings/payment/payment_confirmation_email.html', context)

    email = EmailMultiAlternatives(
        subject='Conferma prenotazione e pagamento - DriveIsland',
        body='Grazie per aver prenotato con DriveIsland.',
        from_email='noreply@driveisland.com',
        to=[booking.user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    return render(request, "bookings/payment/payment_success.html", {"booking": booking})

@login_required
def payment_cancel(request):
    booking_id = request.session.get('last_booking_id')
    if booking_id:
        messages.warning(request, "Hai annullato il pagamento. Puoi riprovarci quando vuoi.")
        return redirect('checkout', booking_id=booking_id)
    else:
        messages.error(request, "Nessuna prenotazione trovata.")
        return redirect('dashboard')

@login_required
def booking_checkout(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if booking.is_paid:
        return redirect('booking_success')  # Se già pagata, va alla conferma

    return render(request, 'bookings/checkout.html', {'booking': booking})

@login_required
def cancel_unpaid_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    if not booking.is_paid:
        logger.info(f'Prenotazione non pagata cancellata: ID {booking.id}')
        booking.delete()
        messages.info(request, 'Prenotazione annullata.')
        return redirect('dashboard')

    return redirect('booking_success')

@require_GET
@login_required
def booked_dates_api(request):
    car_id = request.GET.get('car')
    if not car_id:
        return JsonResponse([], safe=False)

    bookings = Booking.objects.filter(car_id=car_id)
    dates = []
    for booking in bookings:
        current = booking.start_date
        while current <= booking.end_date:
            dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
    return JsonResponse(dates, safe=False)

class DeleteBookingView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'bookings/cancel_booking.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        booking_id = self.kwargs.get('pk')
        return get_object_or_404(Booking, pk=booking_id, user=self.request.user)

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        logger.info(f'Prenotazione cancellata da utente: ID {booking.id}, utente {request.user}')
        booking.delete()
        return redirect(self.success_url)


@login_required
@user_passes_test(is_admin)
def admin_booking(request):
    form = BookingFilterForm(request.GET or None)
    bookings = Booking.objects.select_related('car', 'user').all()
    now_dt = now()


    if form.is_valid():
        if form.cleaned_data['car']:
            bookings = bookings.filter(car=form.cleaned_data['car'])
        if form.cleaned_data['date']:
            d = form.cleaned_data['date']
            bookings = bookings.filter(start_date__lte=d, end_date__gte=d)
        if form.cleaned_data['user']:
            bookings = bookings.filter(user=form.cleaned_data['user'])
    status = request.GET.get('status')
    if status == 'past':
        bookings = bookings.filter(end_date__lt=now_dt.date())
    elif status == 'current':
        bookings = bookings.filter(start_date__lte=now_dt.date(), end_date__gte=now_dt.date())
    elif status == 'future':
        bookings = bookings.filter(start_date__gt=now_dt.date())

    return render(request, 'bookings/admin_booking.html', {
        'form': form,
        'bookings': bookings.order_by('-start_date', 'car__model'),
        'now': now_dt,
        })

@user_passes_test(is_admin)
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    if booking.start_date <= now().date():
        messages.error(request,f"La prenotazione per {booking.car.model} è già iniziata o completata e non può essere annullata.")
        logger.warning(f"Tentativo annullamento fallito per prenotazione ID {booking.id} (già iniziata)")
        return redirect('admin_booking')

    if request.method == 'POST':
        message_template = request.POST.get('reason')
        user_email = booking.user.email
        car_name = booking.car.model

        message = Template(message_template).render(Context({
            'booking': booking,
        }))

        # notifica (email o messaggio interno)
        logger.info(f'Admin {request.user} ha annullato la prenotazione ID {booking.id} per {booking.user}.')
        if user_email:
            logger.info(f'Email di annullamento inviata a {user_email}')
            context = {
                'booking': booking,
                'reason': message,
                'current_year': now().year
            }
            html_message = render_to_string('bookings/cancel_booking_email.html', context)
            email = EmailMultiAlternatives(
                subject='Prenotazione annullata',
                body=message,
                from_email='noreply@driveisland.com',
                to=[user_email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()

        booking.delete()
        messages.success(request, f'Prenotazione per {car_name} annullata.')
        return redirect('admin_booking')

    return render(request, 'bookings/cancel_booking.html', {'booking': booking})