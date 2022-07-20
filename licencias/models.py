from django.db import models

# Create your models here.
class Licencia(models.Model):
    matricula = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=10, null=True)
    modelo = models.CharField(max_length=15, null=True)
    color = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"<Licencia {self.matricula}"