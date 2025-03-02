from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from django.conf import settings
import httpx
import datetime as dt
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
from .models import User, SellerReviews
from products.models import Product
from django.contrib.auth import authenticate

from products.serializers import ProductSerializer
from .serializers import UserRegistrationSerializer, CustomAuthTokenSerializer, UserSerializer, SellerReviewSerializer


@api_view(['POST'])
def register_user(request):
    """Регистрация пользователя с генерацией токенов и авторизацией по email и паролю."""
    # Сериализация данных запроса
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        # Создаем пользователя
        user = serializer.save()

        # Генерация токенов refresh и access
        refresh = RefreshToken.for_user(user)

        # Авторизация пользователя (по email и паролю)
        # Здесь нет необходимости вручную авторизовывать пользователя, так как мы передаем токены

        # Формируем ответ с токенами
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuth(TokenObtainPairView):
    """Кастомная авторизация с email и паролем"""

    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = serializer.get_token(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


def suggest_inn(surname, name, patronymic, birthdate, doctype, docnumber, docdate):
    url = "https://service.nalog.ru/inn-proc.do"
    data = {
        "fam": surname,
        "nam": name,
        "otch": patronymic,
        "bdate": birthdate,
        "bplace": "",
        "doctype": doctype,
        "docno": docnumber,
        "docdt": docdate,
        "c": "innMy",
        "captcha": "",
        "captchaToken": "",
    }
    resp = requests.post(url=url, data=data)
    resp.raise_for_status()
    return resp.json()


@api_view(['POST'])
def check_inn(request):
    # Получаем данные из запроса
    surname = request.data.get('surname')
    name = request.data.get('name')
    patronymic = request.data.get('patronymic')
    birthdate = request.data.get('birthdate')
    docnumber = request.data.get('docnumber')
    docdate = request.data.get('docdate')
    inn_from_front = request.data.get('inn')  # ИНН, который передается с фронта
    doctype = "21"

    # Валидация данных
    if not all([surname, name, patronymic, birthdate, docnumber, docdate, inn_from_front]):
        return JsonResponse({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Получаем ИНН от сервиса налоговой
        response = suggest_inn(
            surname=surname,
            name=name,
            patronymic=patronymic,
            birthdate=birthdate,
            doctype=doctype,
            docnumber=docnumber,
            docdate=docdate
        )

        print(response)
        # Проверяем, совпадает ли ИНН с тем, что передал фронт
        if response['inn'] == inn_from_front:
            user = request.user
            
            # Обновляем данные пользователя
            user.activated = True
            user.inn = inn_from_front
            user.save()
            return JsonResponse({'message': 'INN match success', 'inn': response['inn']}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'INN does not match'}, status=status.HTTP_400_BAD_REQUEST)
    except requests.RequestException as e:
        return JsonResponse({'error': f'Error calling INN service: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SellerReviewCreateView(generics.CreateAPIView):
    queryset = SellerReviews.objects.all()
    serializer_class = SellerReviewSerializer
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи могут оставлять комментарии

    def perform_create(self, serializer):
        # Получаем seller_id из данных запроса
        seller_id = self.request.data.get('seller')
        if not seller_id:
            raise ValidationError("Seller ID is required.")
        
        # Получаем продавца по ID
        seller = get_object_or_404(get_user_model(), id=seller_id)
        
        # Сохраняем отзыв, привязываем его к продавцу через сериализатор
        serializer.save(seller=seller)



@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Доступ только для авторизованных пользователей
def get_my_info(request):
    """Получение информации о пользователе по его ID, его отзывах и товарах."""
    try:
        user = request.user
    except get_user_model().DoesNotExist:
        raise NotFound(detail="User not found.")  # Возвращаем ошибку 404, если пользователь не найден

    # Получаем все отзывы для текущего продавца
    reviews = SellerReviews.objects.filter(seller=user)  # Фильтруем по продавцу (пользователю)

    # Получаем все товары текущего пользователя
    products = Product.objects.filter(seller=user, active=True)  # Только активные товары

    # Используем сериализаторы для отзыва и товаров
    review_serializer = SellerReviewSerializer(reviews, many=True)
    product_serializer = ProductSerializer(products, many=True)

    # Создаем итоговый ответ
    response_data = {
        'user': UserSerializer(user).data,
        'reviews': review_serializer.data,
        'products': product_serializer.data
    }

    return Response(response_data)


@api_view(['GET'])
def get_user_info(request, user_id):
    """Получение информации о пользователе по его ID, его отзывах и товарах."""
    # Попытка получить пользователя по переданному ID
    try:
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        raise NotFound(detail="User not found.")  # Возвращаем ошибку 404, если пользователь не найден

    # Получаем все отзывы для текущего продавца
    reviews = SellerReviews.objects.filter(seller=user)  # Фильтруем по продавцу (пользователю)

    # Получаем все товары текущего пользователя
    products = Product.objects.filter(seller=user, active=True)  # Только активные товары

    # Используем сериализаторы для отзыва и товаров
    review_serializer = SellerReviewSerializer(reviews, many=True)
    product_serializer = ProductSerializer(products, many=True)

    # Создаем итоговый ответ
    response_data = {
        'user': UserSerializer(user).data,
        'reviews': review_serializer.data,
        'products': product_serializer.data
    }

    return Response(response_data)


@api_view(['POST'])
def update_bio(request):
    """Изменить био пользователя"""
    # Получаем данные из запроса
    new_bio = request.data.get('bio')
    
    if not new_bio:
        return Response({'detail': 'bio are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка пользователя по паролю
    user = request.user
    if not user:
        return Response({'detail': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)

    # Обновляем био пользователя
    user.bio = new_bio
    user.save()

    return Response({'detail': 'Bio updated successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_avatar(request):
    """Обновить аватар пользователя в формате Base64"""
    avatar_base64 = request.data.get('avatar')

    if not avatar_base64:
        return Response({'detail': 'Avatar in base64 format is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # try:
    #     # Проверяем, что это валидная строка base64
    #     image_data = base64.b64decode(avatar_base64.split(',')[1])
    #     image = Image.open(BytesIO(image_data))
    # except Exception as e:
    #     return Response({'detail': 'Invalid image data.'}, status=status.HTTP_400_BAD_REQUEST)

    # Сохраняем аватар в поле аватара
    user = request.user  # Получаем текущего пользователя
    user.avatar = avatar_base64  # Сохраняем Base64 строку в поле
    user.save()

    return Response({'detail': 'Avatar updated successfully.'}, status=status.HTTP_200_OK)