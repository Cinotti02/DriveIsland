from django.urls import path
from . import views

urlpatterns = [
    path('contattaci/', views.contact, name='contact'),
    path('admin/messages/', views.admin_inbox, name='admin_inbox'),
    path('admin/messages/<int:message_id>/reply/', views.reply_message, name='reply_message'),
]