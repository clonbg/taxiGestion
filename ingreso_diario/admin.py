from django.contrib import admin
from .models import ingresoDiario

# Register your models here.

@admin.register(ingresoDiario)
class ingresoDiarioAdmin(admin.ModelAdmin):
    list_display=['dia','taxista','total_efectivo','total_apps','total_tpv','varios']
    list_filter=['dia','taxista']