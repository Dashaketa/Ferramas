from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from usuarios.models import CustomUser  # Asegúrate de importar desde la aplicación correcta
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductoForm
from .models import Producto, Carrito, ItemCarrito
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.error.transbank_error import TransbankError
import uuid




def pagina_error(request):
    return render(request, 'pages/pagina_error.html')



# Función para verificar si el usuario es administrador
def es_administrador(user):
    return user.is_authenticated and user.es_administrador

#pagina_pago

def pagina_pago(request):
    return render(request, 'pages/pagina_pago.html')

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



# Vista para agregar los productos en el carrito
@login_required
def agregar_al_carrito(request, producto_id):
    # Asegúrate de que el producto exista
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener o crear el carrito del usuario autenticado
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    # Agregar o incrementar la cantidad del producto en el carrito
    item, item_creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if not item_creado:
        item.cantidad += 1
    item.save()

    # Mostrar un mensaje de éxito
    messages.success(request, f'{producto.nombre} ha sido agregado al carrito.')

    # Redirigir a la página de productos
    return redirect('productos')
# Vista para ver los productos en el carrito
@login_required
def ver_carrito(request):
    # Obtener el carrito del usuario
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()
    total = sum(item.producto.precio * item.cantidad for item in items)

    # Renderizar el HTML de los elementos del carrito
    carrito_items_html = render_to_string('pages/partials/carrito_items.html', {'items': items})

    return JsonResponse({'html': carrito_items_html, 'total': total})

# Vista para eliminar un producto del carrito
@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, f'{item.producto.nombre} ha sido eliminado del carrito.')
    return redirect('ver_carrito')

# Vista para vaciar el carrito
@login_required
def vaciar_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()
    messages.success(request, 'Tu carrito ha sido vaciado.')
    return redirect('ver_carrito')

@login_required
def obtener_total_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in carrito.items.all())
    return JsonResponse({'total': total})


@login_required
def iniciar_pago(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    amount = sum(int(item.producto.precio) * item.cantidad for item in carrito.items.all())
    
    buy_order = f"order_{uuid.uuid4().hex[:15]}"
    session_id = str(request.user.id) if request.user.is_authenticated else "anon"
    return_url = request.build_absolute_uri('/pago/exito/')

    # Configuración de Transbank con el tipo de integración TEST
    tx = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,  # Código de comercio desde settings.py
        api_key=settings.TRANSBANK_API_KEY,              # API Key desde settings.py
        integration_type=IntegrationType.TEST            # Asegúrate de que sea TEST para pruebas
    ))

    try:
        response = tx.create(buy_order=buy_order, session_id=session_id, amount=amount, return_url=return_url)
        return redirect(f"{response['url']}?token_ws={response['token']}")
    except TransbankError as e:
        messages.error(request, "Error al iniciar el pago: " + str(e))
        return redirect('pagina_error')


@login_required
def confirmar_pago(request):
    token = request.GET.get("token_ws")
    if not token:
        messages.error(request, "Error al confirmar el pago. Token no encontrado.")
        return redirect('pagina_error')

    tx = Transaction(WebpayOptions(
        commerce_code=settings.TRANSBANK_COMMERCE_CODE,
        api_key=settings.TRANSBANK_API_KEY,
        integration_type=IntegrationType.TEST
    ))

    try:
        response = tx.commit(token=token)
        if response['status'] == 'AUTHORIZED':
            return render(request, 'pages/exito_pago.html', {'detalle': response})
        else:
            error = f"({response['status']}, {response['response_code']})"
            return render(request, 'pages/error_pago.html', {'error': error})
    except TransbankError as e:
        messages.error(request, f"Error al confirmar la transacción: {e}")
        return redirect('pagina_error')

   
    
    
    
    
    
    
    