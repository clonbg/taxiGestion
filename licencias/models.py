from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Licencia(models.Model):
    num_licencia = models.IntegerField(validators=[
            MaxValueValidator(1000000),
            MinValueValidator(1)
        ], unique=True)
    matricula = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=10, null=True,blank=True)
    modelo = models.CharField(max_length=15, null=True,blank=True)
    color = models.CharField(max_length=15, null=True,blank=True)

    def __str__(self):
        return f"<Licencia {self.matricula}"