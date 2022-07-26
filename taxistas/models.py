from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


# Create your models here
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **estra_fields):
        if not email:
            raise ValueError(_("Email es necesario"))

        email = self.normalize_email(email)

        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new.user.save()

        return new_user

    def create_superuser(self, email, password, **estra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Es necesario ser del staff"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Es necesario ser superusuario"))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_("Es necesario ser un usuario activo"))

        return self.create_user(email, password, **estra_fields)


class User(AbstractUser):
    nombre = models.CharField(max_length=25, unique=True)
