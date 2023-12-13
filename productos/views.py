# Definición de vistas y lógica del controlador para la aplicación de productos.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib.auth import authenticate, login, logout
from .models import Producto, Devolucion
from .forms import ProductoForm, DevolucionForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def signin(request):
    """
    Vista para el inicio de sesión de un usuario.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'signin.html', {'error': 'Credenciales incorrectas'})
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})


def signup(request):
    """
    Vista para el formulario de registro de un nuevo usuario.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {"form": form})

@login_required
def custom_logout(request):
    """
    Vista para cerrar la sesión del usuario.
    """
    logout(request)
    return redirect('home')

def home(request):
    """
    Vista principal que muestra las funciones a realizar en el inventario y permite realizar una búsqueda por nombre
    """
    return render(request, 'home.html')

@login_required
def agregar_producto(request):
    """
    Vista para agregar productos al inventario
    """
    form = ProductoForm()
    mensaje = None
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            mensaje = "Producto agregado exitosamente"
            return redirect('lista_productos')

    data = {'form': form, 'mensaje': mensaje}
    return render(request, 'create_producto.html', data)

@login_required
def obtener_productos(request):
    """
    Vista para mostrar los productos
    """
    productos = Producto.objects.all()
    data = [{'id': producto.id, 'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio, 'stock': producto.stock} for producto in productos]
    return render(request, 'lista_producto.html', {'productos': data})


@login_required
def editar_producto(request, pk):
    """
    Vista para editar un producto en el inventario.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    """
    Vista para eliminar un producto del inventario.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('lista_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})

@login_required
def lista_productos(request):
    """
    Vista para listar todos los productos existentes en la base de datos.
    """
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(Q(nombre__icontains=query))

    for producto in productos:
        if producto.descontar_stock():
            print(f'Alerta: Stock bajo para {producto.nombre}')

    return render(request, 'lista_productos.html', {'productos': productos, 'query': query})



@login_required
@transaction.atomic
def devoluciones(request):
    """
    Vista para realizar una devolución a un cliente.
    """

    if request.method == 'POST':
        form = DevolucionForm(request.POST)
        if form.is_valid():
            devolucion = form.save(commit=False)

            producto = devolucion.producto
            cantidad_devuelta = int(devolucion.cantidad_devuelta)

            if cantidad_devuelta > 0:
                producto.save()
                devolucion.save()
                producto.agregar_devolucion(devolucion.cantidad_devuelta)

            else: 
                messages.error(request, 'La cantidad devuelta debe ser un número positivo')

            return redirect('devoluciones')
    else: 
        form = DevolucionForm()


    devoluciones_list = Devolucion.objects.all().order_by('-fecha_devolucion')

    paginator = Paginator(devoluciones_list, 20)  
    page = request.GET.get('page')

    try:
        devoluciones = paginator.page(page)
    except PageNotAnInteger:
        
        devoluciones = paginator.page(1)
    except EmptyPage:
        
        devoluciones = paginator.page(paginator.num_pages)

    return render(request, 'devoluciones.html', {'form': form, 'devoluciones_list': devoluciones_list})


    