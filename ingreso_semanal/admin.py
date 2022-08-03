from django.contrib import admin
from .models import IngresoSemanal

# Register your models here.

@admin.register(IngresoSemanal)
class IngresoSemanalAdmin(admin.ModelAdmin):
    list_display=['dia_inicio','dia_fin','taxista','total_efectivo_semana','total_apps_semana','total_tpv_semana','varios_semana']
    list_filter=['dia_inicio','dia_fin','taxista']