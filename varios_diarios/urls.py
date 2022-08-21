from django.urls import path
from . import views

urlpatterns=[
    path('create/',views.VariosDiariosCreateView.as_view(), name='varios_diarios'),
    path('<int:vario_diario_id>/',views.VariosDiariosDetailView.as_view(), name='detail_vario_diario')
]