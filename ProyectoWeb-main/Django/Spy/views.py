from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from usuarios.models import CustomUser  # Asegúrate de importar desde la aplicación correcta
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

def home(request):
    context = {
        'es_administrador': request.user.is_authenticated and request.user.es_administrador
    }
    return render(request, 'pages/Home.html', context)

def productos(request):
    return render(request, 'pages/productos.html')

def nosotros(request):
    return render(request, 'pages/Nosotros.html')

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

def es_administrador(user):
    return user.is_authenticated and user.es_administrador

@login_required
@user_passes_test(es_administrador)
def listar_usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'pages/listar_usuarios.html', {'usuarios': usuarios})

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

@login_required
@user_passes_test(es_administrador)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(CustomUser, id=usuario_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('listar_usuarios')

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('inicioSesion')
