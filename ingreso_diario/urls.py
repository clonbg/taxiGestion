from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.ingresoDiarioCreateView.as_view(), name='ingreso_diario'),
]