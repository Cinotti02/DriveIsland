from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from bookings.models import Booking
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next')  # URL richiesta inizialmente
            return redirect(next_url or 'home')  # se non c'è, vai a home
        else:
            messages.error(request, 'Username o password non validi.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrazione completata con successo!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo.')
            return redirect('dashboard')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/dashboard.html', {
        'form': form,
        'bookings': bookings
    })