from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.IngresoDiarioCreateView.as_view(), name='ingreso_diario'),
    path('<int:ingresodiario_id>/',views.IngresoDiarioDetailView.as_view(), name='detail_ingreso_diario')
]