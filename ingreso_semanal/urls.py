from django.urls import path
from . import views

urlpatterns=[
    path('',views.HelloIngresoSemanalView.as_view(),name='Hello_ingreso_semanal')
]