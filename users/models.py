from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

class Roles(models.Model):
    tipo = models.CharField(max_length=20)    

class Usuario(AbstractBaseUser):
    nombre_usu = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    cedula = models.CharField(max_length=20)
    email_usu = models.EmailField(max_length=50, unique=True)
    tel_usu = models.CharField(max_length=15)
    contrasenna = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    id_rol_fk = models.ForeignKey(Roles,null=False, blank=False, default=2,on_delete=models.PROTECT)
    USERNAME_FIELD = 'email_usu'

    objects = UserManager()
    def __str__(self):
        return self.email_usu

