from django.urls import path
from . import views

urlpatterns=[
    path('',views.ReservaCreateListView.as_view(), name='reservas_list'),
]