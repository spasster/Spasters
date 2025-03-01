from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order
from products.models import Product
from .serializers import OrderSerializer

@api_view(['GET'])
def get_all_orders(request):
    """Получить все заказы для пользователя"""
    orders = Order.objects.filter(user=request.user)  # фильтруем по пользователю
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_order(request):
    """Создать новый заказ"""
    # Получаем ID продукта из запроса
    product_id = request.data.get('product_id')
    
    if not product_id:
        return Response({"error": "Product ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем товар
    product = get_object_or_404(Product, id=product_id)

    # Получаем пользователя
    user = request.user  # Предполагаем, что пользователь уже аутентифицирован

    # Сумма заказа равна цене товара
    amount = product.price

    # Создаем заказ с нужными полями
    order = Order.objects.create(
        user=user,
        product=product,
        amount=amount,  # Сумма заказа
        status='paid'   # Статус по умолчанию
    )

    # Возвращаем данные о заказе
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
