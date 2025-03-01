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
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from django.conf import settings
import httpx
import datetime as dt

from .models import User

from .serializers import UserRegistrationSerializer, CustomAuthTokenSerializer, UserSerializer


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


# Функция для проверки ИНН через внешний API
def check_status(inn: str, date: dt.date = None) -> dict:
    """Проверка ИНН через внешнее API."""
    date = date or dt.date.today()
    date_str = date.isoformat()
    url = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
    data = {
        "inn": inn,
        "requestDate": date_str,
    }
    try:
        resp = httpx.post(url=url, json=data)
        return resp.json()
    except httpx.RequestError as e:
        return {"error": f"Ошибка при обращении к API: {e}"}

# Вьюха для добавления ИНН в пользователя
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_inn(request):
    """Функция для добавления ИНН пользователю после проверки через внешний API."""
    inn = request.data.get('inn')

    if not inn:
        return Response({"detail": "ИНН не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка ИНН через API
    response = check_status(inn)
    
    # Проверяем, если ошибка при запросе
    if 'error' in response:
        return Response({"detail": response['error']}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    # Проверяем, что статус ИНН вернул успешный результат
    if not response.get('status'):  # Статус 'OK' - это пример, зависит от структуры ответа
        
        return Response({"detail": "Невалидный ИНН."}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем текущего пользователя
    user = request.user

    # Добавляем ИНН в модель пользователя
    user.inn = inn
    user.activated = True
    user.save()

    return Response({"detail": "ИНН успешно добавлен."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Доступ только для авторизованных пользователей
def get_user_info(request):
    """Получение информации о пользователе."""
    user = request.user  # Получаем текущего пользователя
    serializer = UserSerializer(user)
    return Response(serializer.data)