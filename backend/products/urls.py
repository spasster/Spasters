from django.contrib import admin
from django.urls import path
import products.views as views 

urlpatterns = [
    path('create_product/', views.create_product, name='create_product'),
    path('products/', views.ProductListView.as_view(), name='product-list'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),  # Получить все категории или создать новую
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),  # Создать новую категорию
]