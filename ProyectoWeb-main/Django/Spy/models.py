from django.db import models

# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=9)
    password = models.CharField(max_length=128)
    es_administrador = models.BooleanField(default=False)  # Campo para marcar si el usuario es administrador


    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    
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
    
    