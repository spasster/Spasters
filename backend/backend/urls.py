from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


def ping(request):
    return JsonResponse({'message': 'pong'}, status=200)


schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="Тут будет описание вашего API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/', include('authentaction.urls')),
    path('api/products/', include('products.urls')),

    path('ping/', ping, name='ping'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('swagger-json/', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
