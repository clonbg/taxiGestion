from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from licencias.models import Licencia

# Create your models here


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email es necesario"))

        email = self.normalize_email(email)

        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save()

        return new_user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Es necesario ser del staff"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Es necesario ser superusuario"))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_("Es necesario ser un usuario activo"))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()
    username = None
    first_name = None
    last_name = None
    dni = models.CharField(max_length=25, unique=True)
    nombre = models.CharField(max_length=20)
    apellidos = models.CharField(max_length=50)
    sueldo = models.IntegerField(validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    #foto = models.ImageField()
    licencia = models.ForeignKey(Licencia, on_delete=models.CASCADE, null=True,blank=True)
    email = models.EmailField(max_length=80, unique=True)
    phone_number = PhoneNumberField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['dni', 'nombre', 'apellidos', 'sueldo', 'phone_number']

    def __str__(self):
        return f"<Usuario {self.nombre} {self.apellidos}"
