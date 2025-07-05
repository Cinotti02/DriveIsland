"""
WSGI config for DriveIsland project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DriveIsland.settings')

django.setup()
application = get_wsgi_application()
try:
    call_command('migrate', interactive=False)
    call_command('loaddata', 'backup.json', verbosity=2)
except Exception as e:
    import traceback
    print("=== ERRORE DURANTE IL DEPLOY ===")
    traceback.print_exc()
