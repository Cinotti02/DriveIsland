from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm
from .models import ContactMessage
from django.db.models import Case, When, Value, IntegerField
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.utils.timezone import now
from django.template.loader import render_to_string

def is_admin(user):
    return user.is_authenticated and user.groups.filter(name="Amministratore").exists()

@user_passes_test(is_admin)
def admin_inbox(request):
    messages_list = ContactMessage.objects.annotate(
        priority=Case(
            When(reply='', then=Value(0)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('priority', 'created_at')
    return render(request, 'contact/admin_inbox.html', {'customer_messages': messages_list})

def contact(request):
    first_name = getattr(request.user, 'first_name', '')
    last_name = getattr(request.user, 'last_name', '')
    full_name = f'{first_name} {last_name}'.strip() or getattr(request.user, 'username', '')
    initial = {
        'name': full_name,
        'email': getattr(request.user, 'email', ''),
        'phone': getattr(request.user, 'phone_number', '')
        }

    if request.method == 'POST':
        form = ContactForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                message = form.save(commit=False)
                if request.user.is_authenticated:
                    message.user = request.user  # solo se hai collegato l'utente nel modello
                message.save()
                messages.success(request, "Il tuo messaggio è stato inviato con successo!", extra_tags='user_msg')
                return redirect('contact')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Errore nel modulo. Per favore, correggi i campi evidenziati.", extra_tags='user_msg')
    else:
        form = ContactForm(initial=initial, user=request.user)

    return render(request, 'contact/contact.html', {'form': form})

@user_passes_test(is_admin)
def reply_message(request, message_id):
    msg = get_object_or_404(ContactMessage, pk=message_id)

    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        if reply_text:
            msg.reply = reply_text
            msg.replied_at = now()
            msg.save()

            subject = f"DriveIsland – Abbiamo risposto alla tua richiesta: {msg.subject}"

            # HTML email content
            html_content = render_to_string('contact/email_reply.html', {
                'msg': msg,
                'reply_text': reply_text,
            })

            text_content = f"{reply_text}"

            # Invio email di risposta
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[msg.email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            messages.success(request, "Risposta inviata al cliente.", extra_tags='admin_reply')
            return redirect('admin_inbox')
        else:
            messages.error(request, "Il campo risposta non può essere vuoto.")

    return render(request, 'contact/reply.html', {'msg': msg})