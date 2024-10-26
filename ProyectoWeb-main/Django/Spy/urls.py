from django.urls import path
from Spy import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path('productos/', views.productos, name="productos"),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('inicioSesion/', views.inicioSesion, name='inicioSesion'),
    path('registro/', views.registro, name='registro'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:usuario_id>/actualizar/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    path('logout/', views.cerrarSesion, name='logout'),
]
