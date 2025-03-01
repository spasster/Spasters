from rest_framework import serializers
from .models import Order
from authentaction.models import User
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    # Название товара (связано с моделью через product)
    product_title = serializers.CharField(source='product.title', read_only=True)  # read_only, чтобы не требовалось от клиента
    # Указываем, что эти поля не обязательны
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_title', 'amount', 'status']

    def create(self, validated_data):
        # Убираем user и product из validated_data, так как они передаются вручную в perform_create
        validated_data.pop('user', None)
        validated_data.pop('product', None)
        validated_data.pop('amount', None)
        return super().create(validated_data)
