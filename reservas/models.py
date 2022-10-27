from django.db import models
from taxistas.models import User


class Reserva(models.Model):
    nombre = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    hora_recogida = models.TimeField(null=True, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    taxista = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    confirmada = models.BooleanField(default=False)
    hora_creada_reserva = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"<Reserva {self.nombre}, {self.direccion}, {self.hora}"
