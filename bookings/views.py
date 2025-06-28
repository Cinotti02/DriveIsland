from django.views.generic.edit import CreateView
from .models import Booking
from .forms import BookingForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from datetime import timedelta



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
            initial['car'] = get['car']

        return initial

    def get_success_url(self):
        return reverse_lazy('booking_success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.request.session['last_booking_id'] = self.object.id
        return response

@login_required
def booking_success(request):
    booking_id = request.session.pop('last_booking_id', None)
    if not booking_id:
        return redirect('dashboard')  # fallback se si accede direttamente

    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    return render(request, 'bookings/success.html', {'booking': booking})

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
    template_name = 'bookings/delete_booking.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        booking_id = self.kwargs.get('pk')
        return get_object_or_404(Booking, pk=booking_id, user=self.request.user)

    def post(self, request, *args, **kwargs):
        booking = self.get_object()
        booking.delete()
        return redirect(self.success_url)