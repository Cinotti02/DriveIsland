from django.urls import path
from . import views

urlpatterns = [
    path('cars', views.cars_list, name='cars'),
    path('search/', views.car_search, name='car_search'),
    path('car_details/<int:car_id>', views.car_details, name='car_details'),
    path('<int:car_id>/edit/', views.car_edit, name='edit_car'),
    path('cars/<int:car_id>/delete/', views.delete_car, name='delete_car'),
    path('add/', views.add_car, name='add_car'),
]