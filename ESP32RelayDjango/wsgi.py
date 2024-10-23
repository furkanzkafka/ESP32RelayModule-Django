import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ESP32RelayDjango.settings')

application = get_wsgi_application()
