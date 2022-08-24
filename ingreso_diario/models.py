from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from taxistas.models import User
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class IngresoDiario(models.Model):
    dia = models.DateField(default=now)
    imagen = models.ImageField(
        upload_to='imgs/%Y/%m/%d/', null=True, blank=True)
    total_efectivo = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], null=True, blank=True)
    total_apps = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], null=True, blank=True)
    total_tpv = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(1)
    ], null=True, blank=True)
    vario = ArrayField(models.CharField(max_length=25), null=True, blank=True)
    taxista = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"<Ingreso diario {self.taxista}"
