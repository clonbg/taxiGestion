from django.urls import path
from . import views

urlpatterns=[
    path('',views.HelloTaxistasView.as_view(),name='Hello_taxista'),
    path('registro/',views.UserCreateView.as_view(),name='registro')
]