from rest_framework import serializers
from .models import User, SellerReviews
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from products.serializers import ProductSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    default_user = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'default_user']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            activated=False,
            inn=0
        )
        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Попытка получить пользователя по email
        user = get_user_model().objects.filter(email=email).first()
        
        if user and user.check_password(password):
            # Если пользователь найден и пароль верен, возвращаем его
            return {'user': user}

        raise serializers.ValidationError("Invalid email or password")

    def get_token(self, user):
        return RefreshToken.for_user(user)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'inn', 'activated', 'bio']  # Выводим только email и inn


class SellerReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Информация о пользователе, который оставил отзыв

    class Meta:
        model = SellerReviews
        fields = ['id', 'text', 'seller', 'user']

    def create(self, validated_data):
        user = self.context['request'].user  # Получаем пользователя из запроса
        seller = validated_data.get('seller')  # Получаем продавца из данных

        # Создаем новый отзыв
        return SellerReviews.objects.create(user=user, seller=seller, text=validated_data['text'])


class UserWithReviewsAndProductsSerializer(serializers.ModelSerializer):
    reviews = SellerReviewSerializer(many=True, read_only=True)  # Отзывы для продавца
    products = ProductSerializer(many=True, read_only=True)  # Продукты продавца

    class Meta:
        model = get_user_model()
        fields = ['email', 'inn', 'reviews', 'products']  # Выводим email, inn, отзывы и товары