from django.contrib import admin
from .models import ingresoSemanal

# Register your models here.

@admin.register(ingresoSemanal)
class ingresoSemanalAdmin(admin.ModelAdmin):
    list_display=['dia_inicio','dia_fin','taxista','total_efectivo_semana','total_apps_semana','total_tpv_semana','varios_semana']
    list_filter=['dia_inicio','dia_fin','taxista']