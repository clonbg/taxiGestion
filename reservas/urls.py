from django.urls import path
from . import views

urlpatterns=[
    path('',views.HelloReservasView.as_view(), name='reservas'),
]