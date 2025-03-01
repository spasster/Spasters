from django.contrib import admin
from django.urls import path
import authentaction.views as views 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', views.register_user, name='auth_register'),
    path('login/', views.CustomAuth.as_view(), name='auth_login'),

    path('add_inn/', views.add_inn, name='add_inn'),

    path('user_info/', views.get_user_info, name='get_user_info'),

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),

]