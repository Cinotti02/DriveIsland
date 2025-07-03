from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.BookingCreateView.as_view(), name='create_booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('api/booked-dates/', views.booked_dates_api, name='booked_dates_api'),
    path('admin', views.admin_booking, name='admin_booking'),
    path('admin/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('pagamento-annullato/', views.payment_cancel, name='payment_cancel'),
    path('checkout/<int:booking_id>/', views.booking_checkout, name='checkout'),
    path('checkout/<int:booking_id>/paga/', views.start_payment, name='start_payment'),
    path('pagamento-avvenuto/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('cancel-unpaid/<int:booking_id>/', views.cancel_unpaid_booking, name='cancel_unpaid_booking'),
]
