from django.contrib import admin
from django.urls import path
import authentaction.views as views 

urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
]