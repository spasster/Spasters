<template>
    <div class=" rounded-lg shadow-md p-6">
      <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
        <i class="pi pi-shopping-cart"></i>
        Корзина
      </h2>
  
      <div v-if="!cartItems.length" class="text-gray-500 text-center py-8">
        Ваша корзина пуста
      </div>
  
      <DataTable v-else :value="cartItems" class="mb-6">
        <Column header="Товар">
          <template #body="{ data }">
            <div class="flex items-center gap-3">
              <img 
                v-if="data.image"
                :src="data.image" 
                class="w-16 h-16 object-cover rounded"
                alt="Изображение товара"
              >
              <div>
                <div class="font-semibold">{{ data.name }}</div>
                <div class="text-sm text-gray-500">{{ data.category }}</div>
              </div>
            </div>
          </template>
        </Column>
  
        <Column header="Цена" class="text-right">
          <template #body="{ data }">
            {{ formatCurrency(data.price) }}
          </template>
        </Column>
  
        <Column header="Количество" class="text-center">
          <template #body="{ data }">
            <div class="flex items-center justify-center gap-2">
              <Button 
                icon="pi pi-minus" 
                @click="cart.updateQuantity(data.id, data.quantity - 1)"
                :disabled="data.quantity <= 1"
                severity="secondary"
                outlined
              />
              <span class="w-8 text-center">{{ data.quantity }}</span>
              <Button 
                icon="pi pi-plus"
                @click="cart.updateQuantity(data.id, data.quantity + 1)"
                severity="secondary"
                outlined
              />
            </div>
          </template>
        </Column>
  
        <Column header="Сумма" class="text-right">
          <template #body="{ data }">
            {{ formatCurrency(data.price * data.quantity) }}
          </template>
        </Column>
  
        <Column header="Действия" class="text-center">
          <template #body="{ data }">
            <Button 
              icon="pi pi-trash" 
              severity="danger" 
              @click="cart.removeItem(data.id)" 
              outlined
            />
          </template>
        </Column>
      </DataTable>
  
      <div v-if="cartItems.length" class="border-t pt-4">
        <div class="flex justify-between items-center mb-4">
          <span class="font-semibold">Итого:</span>
          <span class="text-xl font-bold">{{ formatCurrency(cartTotal) }}</span>
        </div>
  
        <Button 
    label="Оформить заказ" 
    icon="pi pi-check" 
    class="w-full" 
    severity="success"
    @click="handleCheckout"
    :disabled="isProcessing"
  >
    <span v-if="!isProcessing">Оформить заказ</span>
    <span v-else>Перенаправляем на оплату...</span>
  </Button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { storeToRefs } from 'pinia';
  import { useCartStore } from '@/stores/cart';
  
  const cart = useCartStore();
  const { cartItems, cartTotal } = storeToRefs(cart);
  const isProcessing = ref(false);
  const { $apiFetch } = useNuxtApp()


  
  const formatCurrency = (value) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 0
    }).format(value);
  };
  
  const handleCheckout = async () => {
  try {
    isProcessing.value = true;
    console.log(cartItems.value[0])
    // Отправляем запрос на получение платежной ссылки
    await $apiFetch(
      '/api/order/orders/create/',
      {
        method: 'POST',
        body: { 
          product_id: cartItems.value[0].id 

        },
      }
    );
    const { data: response } = await useFetch(
      `http://127.0.0.1:8000/payment_url/${cartTotal.value}/`,
      {
        method: 'GET',
        server: false
      }
    );

    if (response.value?.link) {
      // Перенаправляем пользователя на страницу оплаты
      window.location.href = response.value.link;
    } else {
      throw new Error('Не удалось получить ссылку для оплаты');
    }
  } catch (error) {
    console.error('Ошибка при оформлении заказа:', error);
    alert('Произошла ошибка при переходе к оплате. Попробуйте еще раз.');
  } finally {
    isProcessing.value = false;
    cart.clearCart();
  }
};
  </script>
  
  <style scoped>
  :deep(.p-datatable) {
    font-size: 0.9rem;
  }
  

  </style>