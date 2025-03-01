from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse

def ping(request):
    return JsonResponse({'message': 'pong'}, status=200)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/auth/', include('authentaction.urls')),
    path('api/products/', include('products.urls')),

    path('ping/', ping, name='ping'),
]
