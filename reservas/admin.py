from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'hora_recogida']
    list_filter = ['nombre', 'email', 'direccion', 'hora_recogida',
                   'telefono', 'taxista', 'confirmada', 'hora_creada_reserva']
