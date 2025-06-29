from .models import ContactMessage
from .views import is_admin

def unread_messages(request):
    if request.user.is_authenticated and request.user.groups.filter(name="Amministratore").exists():
        return {
            'unread_messages': ContactMessage.objects.filter(reply='').count()
        }
    return {}

def admin_status(request):
    return {
        'is_admin': is_admin(request.user)
    }