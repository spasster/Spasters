from django.contrib import admin
from django.urls import path
import authentaction.views as views 

urlpatterns = [
    path('register/', views.register_user, name='auth_register'),
    path('login/', views.CustomAuth.as_view(), name='auth_login'),

    path('add_inn/', views.add_inn, name='add_inn'),
]