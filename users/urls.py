from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.register_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('booking/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
]