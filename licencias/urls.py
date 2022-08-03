from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.LicenciaCreateView.as_view(), name='licencias'),
    path('<int:licencia_id>/',views.LicenciaDetailView.as_view(), name='detail_licencia')
]