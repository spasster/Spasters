# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('orders/', get_all_orders, name='get_all_orders'),  # Получение всех заказов пользователя
    path('orders/create/', create_order , name='order-create'),  # Создать новый заказ
]
