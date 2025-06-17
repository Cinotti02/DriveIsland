from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.car_search, name='car_search'),
]