from django.urls import path
from Spy import views
from django.contrib.auth.views import LogoutView
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
    path('pagar/', views.pagina_pago, name='pagina_pago'),


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
     
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)