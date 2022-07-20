from django.urls import path
from . import views

urlpatterns=[
    path('',views.HelloIngresoDiarioView.as_view(),name='Hello_ingreso_diario')
]