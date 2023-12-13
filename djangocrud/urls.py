# Configuración de las URL del proyecto Django.
from django.contrib import admin
from django.urls import path, include
from productos import views  
from django.conf import settings
from django.conf.urls.static import static

# Definición de las rutas y vistas del proyecto.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
    path('', views.home, name='home'),
    path('create_producto/',views.agregar_producto, name='create_producto'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'), 
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('obtener_productos/', views.obtener_productos, name='obtener_productos'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),  
    path('devoluciones/', views.devoluciones, name='devoluciones'),
]

# Configuración para servir archivos estáticos durante el desarrollo.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)