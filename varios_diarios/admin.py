from django.contrib import admin
from .models import VariosDiarios

# Register your models here.


@admin.register(VariosDiarios)
class VariosDiariosAdmin(admin.ModelAdmin):
    list_display = [
        'cantidad',
        'concepto',
    ]
    list_filter = [
        'cantidad',
    ]
