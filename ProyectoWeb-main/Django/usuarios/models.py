from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=100, default='NombrePorDefecto')
    apellido = models.CharField(max_length=100, default='ApellidoPorDefecto')
    correo_electronico = models.EmailField(unique=True, default='correo_por_defecto@example.com')
    telefono = models.CharField(max_length=9, default='000000000')
    es_administrador = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
