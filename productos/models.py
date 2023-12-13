# Definición de modelos de la base de datos para la aplicación de productos.
from django.db import models

# Definición de modelos para Producto y Devolucion.
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

    def descontar_stock(self):
        return self.stock <= 10
    
    def agregar_devolucion(self, cantidad_devuelta):
        self.stock += cantidad_devuelta
        self.save()

        # ... (Definición de campos)

class Devolucion(models.Model):
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad_devuelta = models.PositiveIntegerField()
    fecha_devolucion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Devolución de {self.cantidad_devuelta} {self.producto.nombre}'

      # ... (Definición de campos)