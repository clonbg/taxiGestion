from django.contrib import admin
from .models import IngresoDiario

# Register your models here.


@admin.register(IngresoDiario)
class IngresoDiarioAdmin(admin.ModelAdmin):
    list_display = ['dia', 'taxista',
                    'total_efectivo', 'total_apps', 'total_tpv']
    list_filter = ['dia', 'taxista']
