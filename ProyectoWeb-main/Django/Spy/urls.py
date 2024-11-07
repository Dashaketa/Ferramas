from django.urls import path
from Spy import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),

    # Rutas relacionadas con productos
    path('productos/', views.productos, name='productos'),  # Página general de productos
    path('productos/listar/', views.listar_productos, name='listar_productos'),  # Vista para listar productos (solo admin)
    path('productos/crear/', views.crear_producto, name='crear_producto'),  # Vista para crear productos
    path('productos/<int:producto_id>/actualizar/', views.actualizar_producto, name='actualizar_producto'),  # Vista para actualizar productos
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),  # Vista para eliminar productos
    
    # Ruta para obtener el total del carrito
    path('carrito/obtener_total/', views.obtener_total_carrito, name='obtener_total_carrito'),

    # Rutas para la integración con Transbank
    path('pago/iniciar/', views.iniciar_pago, name='iniciar_pago'),  # Iniciar el proceso de pago
    path('pago/exito/', views.confirmar_pago, name='confirmar_pago'),  # Confirmación del pago exitoso

    # Página de pago
    path('pagar/', views.pagina_pago, name='pagina_pago'),

    # Rutas relacionadas con el carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),  # Ver el contenido del carrito
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # Agregar producto al carrito
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),  # Eliminar un producto del carrito
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),  # Vaciar el carrito completo

    # Otras vistas existentes
    path('nosotros/', views.nosotros, name='nosotros'),
    path('inicioSesion/', views.inicioSesion, name='inicioSesion'),
    path('registro/', views.registro, name='registro'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:usuario_id>/actualizar/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('admin-page/', views.admin_page, name='admin_page'),  # Ruta para la página de administración
    path('pagina_error/', views.pagina_error, name='pagina_error'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
