from django.contrib import messages
from django.urls import resolve

class ClearMessagesOnAdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        match = resolve(request.path_info)
        if match.url_name == 'login' and request.path.startswith('/admin/'):
            list(messages.get_messages(request))  # Svuota i messaggi
        return self.get_response(request)