from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from django.utils.timezone import now

# Create your models here.


class IngresoSemanal(models.Model):
    dia_inicio = models.DateField(unique=True)
    dia_fin = models.DateField(default=now,unique=True)
    imagen_semana = models.ImageField(
        upload_to='imgs/%Y/%m/%d/', null=True, blank=True)
    total_efectivo_semana = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],null=True, blank=True)
    total_apps_semana = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],null=True, blank=True)
    total_tpv_semana = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ],null=True, blank=True)
    varios_semana = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000)
    ],null=True, blank=True)
    taxista = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return f"<Ingreso semanal {self.taxista}"