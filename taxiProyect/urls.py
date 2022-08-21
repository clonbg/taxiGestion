from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Api Docs",
      default_version='v1',
      description="How to API works",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('taxistas/',include('taxistas.urls')),
    path('licencias/',include('licencias.urls')),
    path('ingreso_diario/',include('ingreso_diario.urls')),
    path('ingreso_semanal/',include('ingreso_semanal.urls')),
    path('varios_diarios/',include('varios_diarios.urls')),
    path('djoser/', include('djoser.urls.jwt')),
    path('reset_password/',auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_send/',auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('djoser/', include('djoser.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


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