from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product
from rest_framework.exceptions import ValidationError


@api_view(['POST'])
def create_product(request):
    """Создание продукта с фотографиями."""
    serializer = ProductSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        product = serializer.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(active=True)  # Фильтруем по активным продуктам
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Получаем параметры category и type из запроса
        category = self.request.query_params.get('category', None)
        type = self.request.query_params.get('type', None)
        id = self.request.query_params.get('id', None)

        # Если указана категория, фильтруем по ней
        if category:
            queryset = queryset.filter(category=category)

        # Если указан тип, фильтруем по нему
        if type:
            queryset = queryset.filter(type=type)

        # Если указан id, фильтруем по id
        if id:
            queryset = queryset.filter(id=id)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Группируем товары по категориям
        categories = {}
        for product in queryset:
            category = product.category
            if category not in categories:
                categories[category] = []
            categories[category].append(product)

        # Создаем ответ с категориями и товарами в каждой категории
        response_data = []
        for category, products_in_category in categories.items():
            serialized_products = ProductSerializer(products_in_category, many=True).data
            response_data.append({
                'category': category,
                'products': serialized_products
            })

        return Response(response_data)
