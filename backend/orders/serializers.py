from rest_framework import serializers
from .models import Order
from authentaction.models import User
from products.models import Product
from products.serializers import ProductPhotosSerializer

class OrderSerializer(serializers.ModelSerializer):
    # Название товара (связано с моделью через product)
    product_title = serializers.CharField(source='product.title', read_only=True)  # read_only, чтобы не требовалось от клиента
    product_description = serializers.CharField(source='product.description', read_only=True)  # read_only, чтобы не требовалось от клиента
    product_photos = ProductPhotosSerializer(source='product.photos', many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_title', 'product_description', 'amount', 'status', 'product_photos']

    def create(self, validated_data):
        # Убираем user и product из validated_data, так как они передаются вручную в perform_create
        validated_data.pop('user', None)
        validated_data.pop('product', None)
        validated_data.pop('amount', None)
        return super().create(validated_data)
