from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.IngresoDiarioCreateView.as_view(), name='ingreso_diario'),
]