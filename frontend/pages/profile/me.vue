<template>
  <div class="p-4 max-w-4xl mx-auto">
    <!-- Профиль -->
    <div class="flex flex-col md:flex-row items-center gap-4 md:gap-6">
      <div class="relative group">
        <img
          :src="authStore.user.avatar || defaultAvatar"
          alt="Аватар"
          class="w-16 h-16 md:w-24 md:h-24 rounded-full border-4 border-gray-700 object-cover"
        />
        <label
          for="avatar-upload"
          class="absolute inset-0 flex items-center justify-center bg-black/50 group-hover:opacity-100 transition-opacity cursor-pointer rounded-full"
        >
          <i class="pi pi-camera text-white text-xl"></i>
        </label>
        <input
          id="avatar-upload"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleAvatarUpload"
        />
      </div>
      <div class="text-center md:text-left">
        <h2 class="text-xl md:text-2xl font-semibold text-white">{{ user.email }}</h2>
        <p class="text-gray-400">{{ user.bio }}</p>
        <p v-if="user.activated" class="text-gray-400 text-sm">ИНН: {{ user.inn }}</p>
      </div>
      <div class="flex gap-2 md:ml-auto mt-2 md:mt-0">
        <Button 
          label="Редактировать"
          icon="pi pi-pencil" 
          class="p-button-sm md:p-button" 
          @click="showEditDialog = true" 
        />
        <Button 
          label="Выйти" 
          severity="danger" 
          icon="pi pi-sign-out" 
          class="p-button-sm md:p-button" 
          @click="authStore.logout(); navigateTo('/')" 
        />
      </div>
    </div>

    <!-- Табы -->
    <div class="mt-6 card">
      <Tabs value="active" scrollable>
        <TabList class="flex flex-wrap">
          <Tab value="active">Активные товары</Tab>
          <Tab value="history">История заказов</Tab>
          <Tab value="reviews">Отзывы</Tab>
        </TabList>

        <TabPanels>
          <!-- Активные товары -->
          <TabPanel value="active">
            <div v-if="user.activated" class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card 
                v-for="product in authStore.products" 
                :key="product.id" 
                class="relative hover:shadow-lg transition-shadow"
              >
                <template #content>
                  <img 
                    :src="product.photos[0]?.photo || '/product-placeholder.jpg'"
                    class="w-full h-32 object-cover rounded-lg mb-4"
                  />
                  <h3 class="text-lg font-semibold">{{ product.title }}</h3>
                  <p class="text-gray-400 text-sm mt-2 line-clamp-2">
                    {{ product.description }}
                  </p>
                  <div class="flex justify-between items-center mt-4">
                    <span class="text-primary font-bold">
                      {{ product.price?.toLocaleString('ru-RU') }} ₽
                    </span>
                    <Tag 
                      :value="product.active ? 'Активен' : 'Неактивен'"
                      :severity="product.active ? 'success' : 'danger'"
                    />
                  </div>
                  <div class="mt-4 flex gap-2 justify-end">
                    <Button 
                      icon="pi pi-pencil" 
                      class="p-button-sm p-button-outlined"
                      @click="editProduct(product.id)"
                    />
                    <Button 
                      icon="pi pi-trash" 
                      class="p-button-sm p-button-danger p-button-outlined"
                      @click="confirmDelete(product.id)"
                    />
                  </div>
                </template>
              </Card>

              <div 
                v-if="!authStore.products.length" 
                class="col-span-full text-center py-4"
              >
                <p class="text-gray-400">Нет активных товаров</p>
              </div>

              <CreateProduct class="col-span-full" />

              <!-- <NuxtLink to="/profile/create" class="col-span-full">
                <Button 
                  label="Добавить товар" 
                  icon="pi pi-plus" 
                  class="w-full mt-4"
                />
              </NuxtLink> -->
            </div>

            <!-- Блок верификации -->
            <div v-else class="verification-block">
              <div class="verification-message">
                <i class="pi pi-info-circle"></i>
                <h3>Для публикации товаров требуется верификация</h3>
                <p>Пройдите проверку документов для доступа к полному функционалу</p>
                <Verif @verified="handleVerificationComplete" />
              </div>
            </div>
          </TabPanel>

          <!-- История заказов -->
          <TabPanel value="history">
            <div v-if="loadingOrders" class="text-center py-8">
              <ProgressSpinner />
            </div>

            <div v-else-if="orderError" class="text-red-500 text-center py-8">
              {{ orderError }}
            </div>

            <div v-else>
              <div v-if="!orders.length" class="text-center py-8">
                <p class="text-gray-400">Нет завершенных заказов</p>
              </div>

              <div v-else class="space-y-4">
                <Card 
                  v-for="order in orders" 
                  :key="order.id" 
                  class="relative hover:shadow-lg transition-shadow"
                >
                  <template #content>
                    <div class="flex justify-between items-start mb-4">
                      <div>
                        <h3 class="text-lg font-semibold">Заказ #{{ order.id }}</h3>
                        <p class="text-gray-500 text-sm">
                          {{ formatDate(order.created_at) }}
                        </p>
                      </div>
                      <Tag 
                        :value="order.status"
                        :severity="getStatusSeverity(order.status)"
                      />
                    </div>

                    <div class="grid gap-2">
                      <div 
                        v-for="item in order.items" 
                        :key="item.id" 
                        class="flex justify-between"
                      >
                        <span>{{ item.product.title }}</span>
                        <span class="font-semibold">
                          {{ item.quantity }} × {{ item.price.toLocaleString('ru-RU') }} ₽
                        </span>
                      </div>
                    </div>

                    <Divider />

                    <div class="flex justify-between items-center mt-4">
                      <span class="font-semibold">Итого:</span>
                      <span class="text-xl text-primary">
                        {{ order.amount.toLocaleString('ru-RU') }} ₽
                      </span>
                    </div>
                  </template>
                </Card>
              </div>
            </div>
          </TabPanel>

          <!-- Отзывы -->
          <TabPanel value="reviews">
            <div class="space-y-4">
              <div 
                v-for="review in authStore.reviews" 
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
          </TabPanel>
        </TabPanels>
      </Tabs>
    </div>

    <!-- Диалог редактирования профиля -->
    <Dialog v-model:visible="showEditDialog" header="Редактирование профиля" :modal="true">
      <div class="flex flex-col gap-4">
        <div v-if="userType === 'seller'">
          <label class="block text-gray-300">ИНН</label>
          <InputNumber 
            v-model="user.inn" 
            :useGrouping="false" 
            class="w-full" 
            placeholder="Введите ИНН"
          />
        </div>
        <div>
          <label class="block text-gray-300 pb-1">Введите БИО</label>
          <Textarea 
            id="description" 
            v-model="bio" 
            rows="5" 
            autoResize
            placeholder="Расскажите о себе"
            class="w-full"
            :disabled="isLoading"
          />
        </div>
        <small v-if="errorMessage" class="text-red-400">{{ errorMessage }}</small>
      </div>
      <template #footer>
        <Button 
          label="Сохранить" 
          :loading="isLoading" 
          icon="pi pi-check" 
          @click="updateBio"
        />
      </template>
    </Dialog>
  </div>
</template>

<script lang="ts" setup>
definePageMeta({ middleware: 'auth' });

import { ref, computed, onMounted } from "vue";
import { format } from 'date-fns';
import { useAuthStore } from '~/stores/auth';

const { $apiFetch } = useNuxtApp()
const authStore = useAuthStore();
const defaultAvatar = "/user.png";
const { navigateTo } = useRouter();

// Состояния для истории заказов
const orders = ref([]);
const loadingOrders = ref(false);
const orderError = ref('');

// Состояния для аватарки
const avatarLoading = ref(false);
const avatarError = ref('');

// Данные пользователя
const user = computed(() => authStore.user);

// Инициализация bio текущим значением
const bio = ref(user.value.bio || '');

// Редактирование профиля
const showEditDialog = ref(false);
const isLoading = ref(false);
const errorMessage = ref("");

// Загрузка заказов
const fetchOrders = async () => {
  try {
    loadingOrders.value = true;
    orderError.value = '';
    
    const response = await $apiFetch('/api/order/orders/');
    orders.value = response;
  } catch (error) {
    orderError.value = 'Не удалось загрузить историю заказов';
    console.error('Order history error:', error);
  } finally {
    loadingOrders.value = false;
  }
};

// Обработка загрузки аватарки
const handleAvatarUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  
  if (!file) return;

  // Валидация файла
  if (!file.type.startsWith('image/')) {
    avatarError.value = 'Пожалуйста, выберите изображение';
    return;
  }

  if (file.size > 2 * 1024 * 1024) {
    avatarError.value = 'Максимальный размер файла - 2MB';
    return;
  }

  try {
    avatarLoading.value = true;
    avatarError.value = '';

    // Чтение файла как base64
    const reader = new FileReader();
    reader.readAsDataURL(file);
    
    const base64 = await new Promise((resolve, reject) => {
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });

    // Отправка на сервер
    const response = await $apiFetch('/api/auth/update_avatar/', {
      method: 'POST',
      body: { avatar: base64 }
    });

    // Обновление аватара в хранилище
    authStore.user.avatar = base64;
    
  } catch (error) {
    avatarError.value = 'Ошибка при загрузке аватарки';
    console.error('Avatar upload error:', error);
  } finally {
    avatarLoading.value = false;
    input.value = ''; // Сброс input
  }
};

// Определение цвета статуса
const getStatusSeverity = (status: string) => {
  switch(status.toLowerCase()) {
    case 'completed': return 'success';
    case 'processing': return 'info';
    case 'cancelled': return 'danger';
    default: return 'warning';
  }
};

// Форматирование даты
const formatDate = (dateString: string) => {
  try {
    return format(new Date(dateString), 'dd.MM.yyyy HH:mm');
  } catch {
    return 'Дата неизвестна';
  }
};

// Метод для обновления BIO
const updateBio = async () => {
  if (!bio.value.trim()) {
    errorMessage.value = 'БИО не может быть пустым';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await $apiFetch('/api/auth/update_bio/', {
      method: 'POST',
      body: { bio: bio.value }
    });

    // Обновляем данные пользователя в хранилище
    authStore.user.bio = bio.value;
    showEditDialog.value = false;
  } catch (error) {
    errorMessage.value = error.data?.message || 'Ошибка при обновлении профиля';
    console.error('Update bio error:', error);
  } finally {
    isLoading.value = false;
  }
};

// Загрузка данных при монтировании
onMounted(async () => {
  if (!authStore.user) {
    await authStore.fetchUser();
  }
  await fetchOrders();
});

// Действия с товарами
const editProduct = (id: number) => {
  navigateTo(`/profile/edit/${id}`);
};

const confirmDelete = async (id: number) => {
  if (confirm('Вы уверены что хотите удалить товар?')) {
    try {
      await $fetch(`/api/products/${id}`, { method: 'DELETE' });
      await authStore.fetchUser();
    } catch (error) {
      console.error('Ошибка удаления товара:', error);
    }
  }
};
</script>

<style scoped>
.verification-block {
  @apply p-6 border-l-4 rounded-lg mt-4;
}

.verification-message {
  @apply flex flex-col items-center text-center gap-3;
}

.verification-message i {
  @apply text-yellow-500 text-4xl;
}

.verification-message h3 {
  @apply text-xl font-semibold;
}

.verification-message p {
  @apply max-w-md;
}

.review-item {
  @apply border shadow-sm rounded-lg p-4;
}

.review-text {
  @apply text-gray-700 dark:text-gray-300;
}

.pi-camera {
  transition: transform 0.2s;
}

.group:hover .pi-camera {
  transform: scale(1.2);
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