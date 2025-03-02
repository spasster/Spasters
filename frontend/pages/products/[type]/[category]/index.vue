<template>
    <div>
      <!-- Загрузка -->
      <div v-if="pending" class="text-center p-8">
        <ProgressSpinner />
      </div>
  
      <!-- Ошибка -->
      <div v-else-if="error" class="text-red-500 text-center p-8">
        Ошибка загрузки: {{ error.message }}
      </div>
  
      <!-- Контент -->
      <div v-else>
        <h1 class="text-3xl font-bold mb-6">Категория: {{ categoryName }}</h1>
  
        <ProductsList :products="mappedProducts" />
        
        <div v-if="!mappedProducts.length" class="text-center text-gray-500 p-8">
          Нет товаров в этой категории
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  import ProductsList from '@/components/ProductsList.vue'; // путь к компоненту ProductsList
  
  const route = useRoute();
  
  // Получаем категорию и тип из URL параметров
  const category = computed(() => route.params.category);
  const type = computed(() => route.params.type);
  
  // Формируем URL для запроса
  const apiUrl = computed(() =>
    `http://127.0.0.1:8000/api/products/products/?type=${type.value}&category=${category.value}`
  );
  
  // Делаем запрос
  const { data, pending, error } = await useFetch(apiUrl);
  
  // Обрабатываем данные
  const categoryName = computed(() => {
    if (data.value?.[0]?.category) {
      return data.value[0].category;
    }
    return decodeURIComponent(category.value as string);
  });
  
  // Маппим данные под нужный формат для компонента ProductsList
  const mappedProducts = computed(() => {
    return data.value?.flatMap((category) =>
      category.products.map((product) => ({
        id: product.id,
        name: product.title, // Используем title как имя
        type: product.type,
        category: product.category,
        price: product.price,
        inventoryStatus: '', // Пример: если товар активен, он в наличии
        image: product.photos[0]?.photo || '', // Используем первое фото (если оно есть)
        rating: 5, // Поставим 0, если рейтинг не передается
      }))
    ) || [];
  });
  </script>
  
  <style scoped>
  /* Стиль для загрузки, ошибки и контента */
  </style>
  