# Definición de formularios Django para la aplicación de productos.
from django import forms
from .models import Producto, Devolucion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Definición de formularios para productos y devoluciones.
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'stock', 'imagen', 'precio']
    stock = forms.IntegerField(validators=[MinValueValidator(0)])

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion
        fields = ['producto', 'cantidad_devuelta']

    cantidad_devuelta = forms.IntegerField(min_value=1)

