<template>
    <div class="px-5 mx-auto rounded-lg shadow-md">
      <h2 class="text-xl font-semibold mb-4">Оставить отзыв</h2>
      
      <!-- Компонент рейтинга -->
      <div class="mb-4">
        <label class="block text-gray-700 mb-2">Ваша оценка:</label>
        <Rating 
          v-model="rating"
          :cancel="false"
          class="[&>.p-rating-item]:text-2xl [&>.p-rating-item.p-rating-item-active]:text-yellow-500"
        />
        <p v-if="errors.rating" class="text-red-500 text-sm mt-1">{{ errors.rating }}</p>
      </div>
  
      <!-- Поле для комментария -->
      <div class="mb-4">
        <label class="block text-gray-700 mb-2">Ваш комментарий:</label>
        <textarea
          v-model="comment"
          class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2"
          rows="4"
          placeholder="Напишите ваш отзыв..."
        ></textarea>
        <p v-if="errors.comment" class="text-red-500 text-sm mt-1">{{ errors.comment }}</p>
      </div>
  
      <!-- Кнопка отправки -->
      <Button
        @click="handleSubmit"
        class="w-full py-2 px-4 rounded-md"
        :disabled="isSubmitting"
      >
        <span v-if="!isSubmitting">Отправить отзыв</span>
        <span v-else>Отправка...</span>
      </Button>
  
      <!-- Сообщение об успехе -->
      <div v-if="successMessage" class="mt-4 p-3 bg-green-100 text-green-700 rounded-md">
        {{ successMessage }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  const route = useRoute();
  const { $apiFetch } = useNuxtApp();
  
  const rating = ref(0);
  const comment = ref('');
  const errors = ref({
    rating: '',
    comment: '',
    server: ''
  });
  const isSubmitting = ref(false);
  const successMessage = ref('');
  
  const validate = () => {
    let valid = true;
    errors.value = { rating: '', comment: '', server: '' };
  
    if (rating.value === 0) {
      errors.value.rating = 'Пожалуйста, выберите оценку';
      valid = false;
    }
  
    if (!comment.value.trim()) {
      errors.value.comment = 'Пожалуйста, напишите комментарий';
      valid = false;
    }
  
    return valid;
  };
  
  const handleSubmit = async () => {
    if (!validate()) return;
  
    isSubmitting.value = true;
    errors.value.server = '';
    successMessage.value = '';
  
    try {
      const response = await $apiFetch('/api/auth/reviews/', {
        method: 'POST',
        body: {
          text: comment.value.trim(),
          seller: route.params.id
                }
      });
  
      // Сброс формы при успешной отправке
      rating.value = 0;
      comment.value = '';
      successMessage.value = 'Отзыв успешно отправлен!';
      
    } catch (error) {
      if (error.data) {
        // Обработка ошибок валидации с сервера
        for (const [field, messages] of Object.entries(error.data)) {
          errors.value[field] = messages.join(', ');
        }
      } else {
        errors.value.server = 'Ошибка при отправке отзыва. Попробуйте позже.';
      }
    } finally {
      isSubmitting.value = false;
    }
  };
  </script>