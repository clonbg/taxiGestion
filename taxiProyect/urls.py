from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('taxistas/',include('taxistas.urls')),
    path('licencias/',include('licencias.urls')),
    path('ingreso_diario/',include('ingreso_diario.urls')),
    path('ingreso_semanal/',include('ingreso_semanal.urls')),
    path('djoser/', include('djoser.urls.jwt')),
    path('reset_password/',auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #path('djoser/', include('djoser.urls')),
]


"""
# djoser

/users/
/users/me/
/users/confirm/
/users/resend_activation/
/users/set_password/
/users/reset_password/
/users/reset_password_confirm/
/users/set_username/
/users/reset_username/
/users/reset_username_confirm/
/token/login/ (Token Based Authentication)
/token/logout/ (Token Based Authentication)
/jwt/create/ (JSON Web Token Authentication)
/jwt/refresh/ (JSON Web Token Authentication)
/jwt/verify/ (JSON Web Token Authentication)

# taxistas

taxistas/registro/

# licencias

licencias/create/
"""