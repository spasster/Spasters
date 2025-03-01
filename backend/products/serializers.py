from rest_framework import serializers
from .models import *


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = ['id', 'photo']  # Возвращаем только id и фото как строку base64

    def create(self, validated_data):
        return ProductPhotos.objects.create(**validated_data)




class ProductSerializer(serializers.ModelSerializer):
    photos = ProductPhotosSerializer(many=True, required=False)  # Используем сериализатор для фоток

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'type', 'category', 'description', 'active', 'photos', 'number']

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])  # Извлекаем фотографии, если они есть
        user = self.context['request'].user  # Получаем текущего пользователя из контекста

        # Создаем новый продукт
        product = Product.objects.create(seller=user, **validated_data)

        # Создаем фотографии, если они были переданы
        for photo_data in photos_data:
            ProductPhotos.objects.create(product=product, photo=photo_data['photo'])

        return product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
