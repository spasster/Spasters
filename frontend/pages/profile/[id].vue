<template>
    <div class="p-4 max-w-4xl mx-auto">
      <!-- Загрузка -->
      <div v-if="pending" class="text-center p-8">
        <ProgressSpinner />
      </div>
  
      <!-- Ошибка -->
      <div v-else-if="error" class="text-red-500 text-center p-8">
        Ошибка загрузки профиля: {{ error.message }}
      </div>
  
      <!-- Контент -->
      <div v-else>
        <!-- Профиль -->
        <div class="flex flex-col md:flex-row items-center gap-4 md:gap-6">
          <div class="relative group">
            <img
              :src="sellerData.user.avatar || defaultAvatar"
              alt="Аватар"
              class="w-16 h-16 md:w-24 md:h-24 rounded-full border-4 border-gray-700"
            />
          </div>
          <div class="text-center md:text-left">
            <h2 class="text-xl md:text-2xl font-semibold text-white">{{ sellerData.user.email }}</h2>
            <p class="text-gray-400">{{ sellerData.user.bio }}</p>

            <p v-if="sellerData.user.activated" class="text-gray-400 text-sm">ИНН: {{ sellerData.user.inn }}</p>
          </div>
        </div>
  
        <!-- Табы -->
        <div class="mt-6 card">
          <Tabs value="reviews">
            <TabList class="flex flex-wrap">
              <Tab value="reviews">Отзывы</Tab>
              <Tab v-if="sellerData.user.activated" value="tovari">Товары</Tab>
            </TabList>
            <TabPanels>
              <!-- Отзывы -->
              <TabPanel value="reviews">
                <div class="space-y-4">
                  <div 
                    v-for="review in sellerData.reviews" 
                    :key="review.id" 
                    class="p-4 rounded-lg review-item"
                  >
                    <div class="flex items-center gap-2 mb-2">
                      <span class="text-primary">{{ review.user.email }}</span>
                      <Rating :modelValue="5" readonly :cancel="false" />
                      <span class="text-sm text-gray-400 ml-auto">{{ formatDate("02.03.2025") }}</span>
                    </div>
                    <p class="review-text">{{ review.text }}</p>
                  </div>
                </div>
                <SendReview class="pt-3" />
              </TabPanel>
              <TabPanel v-if="sellerData.user.activated" value="tovari">
            <div  class="">
              
              <ProductsList :products="modifiedProducts" />

              <div 
                v-if="!sellerData.products.length" 
                class="col-span-full text-center py-4"
              >
                <p class="text-gray-400">Нет активных товаров</p>
              </div>
            </div>

       
          </TabPanel>
            </TabPanels>
          </Tabs>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { format } from 'date-fns';

  const modifiedProducts = computed(() => {
  return sellerData.value.products.map(product => ({
    ...product,
    image: product.photos[0]?.photo
  }))
})
  
  const route = useRoute();
  const router = useRouter();
  const defaultAvatar = "/user.png";
  
  // Получение ID продавца из URL
  const sellerId = computed(() => route.params.id);
  
  // Запрос данных продавца
  const { data: sellerData, pending, error } = useFetch(
    () => `http://127.0.0.1:8000/api/auth/seller_info/${sellerId.value}/`,
    {
      server: false,
      lazy: true,
      onResponseError({ response }) {
        if (response.status === 404) {
          router.push('/404');
        }
      }
    }
  );

  
  // Форматирование даты
  const formatDate = (dateString: string) => {
    return format(new Date(dateString), 'dd.MM.yyyy');
  };
  </script>
  
  <style scoped>
  .review-item {
    @apply border shadow-sm rounded-lg p-4;
  }
  
  .review-text {
    @apply text-gray-700 dark:text-gray-300;
  }
  
  @media (max-width: 640px) {
    .p-tabview-nav {
      @apply flex-col;
    }
    
    .p-tabview-nav-link {
      @apply w-full;
    }
  }
  </style>