# Configuración de la interfaz de administración de Django.

from django.contrib import admin
from .models import Producto

# Configuración personalizada para la administración de modelos.
class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ['nombre', 'descripcion', 'stock', 'imagen', 'precio']

admin.site.register(Producto, ProductoAdmin)