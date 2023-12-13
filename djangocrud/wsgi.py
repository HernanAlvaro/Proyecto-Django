# Configuración del servidor WSGI para el proyecto Django.
import os
from django.core.wsgi import get_wsgi_application

# Configuración del entorno para el archivo de configuración de Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')

# Obtención de la aplicación WSGI para el proyecto.
application = get_wsgi_application()
