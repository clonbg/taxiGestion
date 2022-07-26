from django.contrib import admin
from .models import User


@admin.register(User)
class TaxistaAdmin(admin.ModelAdmin):
    list_display = ['dni', 'nombre', 'apellidos', 'sueldo', 'phone_number']
    list_filter = ['dni', 'nombre', 'apellidos']
