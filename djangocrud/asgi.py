# Configuración ASGI para el proyecto Django.

import os
from django.core.asgi import get_asgi_application

# Configuración del entorno para el archivo de configuración de Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangocrud.settings')

# Obtención de la aplicación ASGI para el proyecto.
application = get_asgi_application()
