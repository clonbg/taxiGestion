from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('taxistas/',include('taxistas.urls')),
    path('licencias/',include('licencias.urls')),
    path('ingreso_diario/',include('ingreso_diario.urls')),
    path('ingreso_semanal/',include('ingreso_semanal.urls')),
    path('taxistas/', include('djoser.urls')),
]


"""
API
taxistas/registros/
licencias/create
"""