from django.contrib import admin
from .models import Licencia

# Register your models here.

@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    list_display=['num_licencia','matricula','marca','modelo','color']
    list_filter=['marca','modelo','color']