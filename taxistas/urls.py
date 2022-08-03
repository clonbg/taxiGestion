from django.urls import path
from . import views

# taxistas/
urlpatterns=[
    path('registro/',views.UserCreateView.as_view(),name='registro'),
    path('<int:user_id>/',views.UserDetailView.as_view(), name='detail_user')
]