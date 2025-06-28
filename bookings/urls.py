from django.urls import path
from .views import BookingCreateView, booking_success, booked_dates_api

urlpatterns = [
    path('new/', BookingCreateView.as_view(), name='create_booking'),
    path('success/', booking_success, name='booking_success'),
    path('api/booked-dates/', booked_dates_api, name='booked_dates_api'),
]