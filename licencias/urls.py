from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.LicenciaCreateView.as_view(), name='licencias')
]