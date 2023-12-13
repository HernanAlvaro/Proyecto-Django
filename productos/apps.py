# Configuración de la aplicación Django.
from django.apps import AppConfig
from pymongo import MongoClient

# Configuración específica para la aplicación de productos.
class ProductosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productos'
