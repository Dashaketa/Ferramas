from django.db import models
from django.conf import settings


# Create your models here.


#EL modelo que uso para crear los usuarios
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=9)
    password = models.CharField(max_length=128)
    es_administrador = models.BooleanField(default=False)  # Campo para marcar si el usuario es administrador


    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    

#EL modelo que uso para crear los productos

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Campo para imagen subida
    imagen_url = models.URLField(max_length=200, blank=True, null=True)  # Campo para URL de la imagen
    disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
# Modelo del Carrito de Compras
class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrito')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.nombre}"

# Modelo para los Items del Carrito
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def total(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
    
