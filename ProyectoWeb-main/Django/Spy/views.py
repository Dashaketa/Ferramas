from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from usuarios.models import CustomUser  # Asegúrate de importar desde la aplicación correcta
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductoForm
from .models import Producto

# Función para verificar si el usuario es administrador
def es_administrador(user):
    return user.is_authenticated and user.es_administrador

#pagina_pago

def pagina_pago(request):
    return render(request, 'pagina_pago.html')

# Vista de inicio
def home(request):
    context = {
        'es_administrador': request.user.is_authenticated and request.user.es_administrador
    }
    return render(request, 'pages/Home.html', context)

# Vista de productos
def productos(request):
    productos = Producto.objects.all()  # Obtenemos todos los productos de la base de datos

    return render(request, 'pages/productos.html',{'productos': productos})

# Vista de información sobre la empresa
def nosotros(request):
    return render(request, 'pages/Nosotros.html')

# Vista para el inicio de sesión
def inicioSesion(request):
    if request.method == 'POST':
        correo_electronico = request.POST['correo_electronico']
        password = request.POST['password']

        user = authenticate(request, username=correo_electronico, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('home')
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    
    return render(request, 'pages/InicioSesion.html')

# Vista para el registro de usuarios
def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo_electronico = request.POST['correo_electronico']
        telefono = request.POST['telefono']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        es_administrador = 'es_administrador' in request.POST

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('registro')

        usuario = CustomUser(
            username=correo_electronico,
            nombre=nombre,
            apellido=apellido,
            correo_electronico=correo_electronico,
            telefono=telefono,
            password=make_password(password),
            es_administrador=es_administrador
        )
        usuario.save()
        messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect('inicioSesion')

    return render(request, 'pages/registro.html')

# Vista para listar usuarios (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def listar_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'pages/listar_usuarios.html', {'usuarios': usuarios})

# Vista para crear un usuario (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo_electronico = request.POST['correo_electronico']
        telefono = request.POST['telefono']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('crear_usuario')

        usuario = CustomUser(
            username=correo_electronico,
            nombre=nombre,
            apellido=apellido,
            correo_electronico=correo_electronico,
            telefono=telefono,
            password=make_password(password)
        )
        usuario.save()
        messages.success(request, 'Usuario creado exitosamente.')
        return redirect('listar_usuarios')

    return render(request, 'pages/crear_usuario.html')

# Vista para actualizar un usuario (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def actualizar_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)

    if request.method == 'POST':
        usuario.nombre = request.POST['nombre']
        usuario.apellido = request.POST['apellido']
        usuario.correo_electronico = request.POST['correo_electronico']
        usuario.telefono = request.POST['telefono']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('actualizar_usuario', usuario_id=usuario.id)

        usuario.password = make_password(password)
        usuario.save()
        messages.success(request, 'Usuario actualizado exitosamente.')
        return redirect('listar_usuarios')

    return render(request, 'pages/actualizar_usuario.html', {'usuario': usuario})

# Vista para eliminar un usuario (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('listar_usuarios')

# Vista para cerrar sesión
@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('inicioSesion')

# Nueva vista para crear productos (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)

            # Verificar si se proporciona una imagen o una URL
            if producto.imagen_url and not producto.imagen:
                # Prioriza la URL si existe y no se cargó un archivo
                producto.imagen = None
            elif producto.imagen and not producto.imagen_url:
                # Prioriza la imagen cargada desde el dispositivo
                producto.imagen_url = None

            producto.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'pages/crear_producto.html', {'form': form})

# Nueva vista para listar productos (acceso solo para administradores)
@login_required
@user_passes_test(es_administrador)
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'pages/listar_productos.html', {'productos': productos})

# Nueva vista para actualizar un producto (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('listar_productos')
        else:
            messages.error(request, 'Corrige los errores del formulario.')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'pages/actualizar_producto.html', {'form': form})

# Nueva vista para eliminar un producto (solo para administradores)
@login_required
@user_passes_test(es_administrador)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('listar_productos')
    return render(request, 'pages/eliminar_producto.html', {'producto': producto})



def admin_page(request):
    return render(request, 'pages/mediador.html')