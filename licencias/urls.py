from django.urls import path
from . import views

urlpatterns=[
    path('',views.HelloLicenciasView.as_view(),name='Hello_licencia')
]