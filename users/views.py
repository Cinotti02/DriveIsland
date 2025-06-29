from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.urls import reverse
from bookings.models import Booking
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            login(request, user)

            mail_subject = 'Conferma la tua registrazione su DriveIsland'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            activation_link = request.build_absolute_uri(
                reverse('activate', kwargs={'uidb64': uid, 'token': token})
            )

            message = render_to_string('users/send_email.html', {
                'user': user,
                'activation_link': activation_link,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.content_subtype = 'html'
            email.send()

            return render(request, 'users/activation_email.html', {'email': user.email})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account attivato con successo! Ora puoi effettuare il login.')
        return redirect('login')
    else:
        messages.error(request, 'Link di attivazione non valido.')
        return redirect('login')


@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user)
    today = now().date()

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
        'bookings': bookings,
        'today': today
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.start_date <= now().date():
        messages.error(request, "Non puoi disdire una prenotazione già iniziata o passata.")
    else:
        booking.delete()
        messages.success(request, "Prenotazione disdetta con successo.")

    return redirect('dashboard')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = request.user
            today = now().date()

            # Cancella prenotazioni future
            Booking.objects.filter(user=user, start_date__gt=today).delete()

            # Le prenotazioni passate restano ma con user = None
            Booking.objects.filter(user=user, start_date__lte=today).update(user=None)

            logout(request)
            user.delete()
            messages.success(request, 'Il tuo account e le prenotazioni future sono stati eliminati.')
            return redirect('home')
        else:
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profilo aggiornato con successo.')
                return redirect('dashboard')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'form': form})
