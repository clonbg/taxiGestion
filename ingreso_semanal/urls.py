from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.IngresoSemanalCreateView.as_view(), name='ingreso_semanal'),
    path('<int:ingresosemanal_id>/',views.IngresoSemanalDetailView.as_view(), name='detail_ingreso_semanal')
]