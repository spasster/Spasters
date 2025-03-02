<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4">
    <Card class="w-full max-w-md">
      <template #title>
        <div class="text-2xl font-bold">Регистрация</div>
      </template>
      <template #content>
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="flex flex-col gap-2">
            <label for="email" class="font-medium">Email</label>
            <InputText
              id="email"
              v-model="credentials.email"
              type="email"
              placeholder="Ваш email"
              class="w-full"
            />
          </div>

          <div class="flex flex-col gap-2">
            <label for="password" class="font-medium">Пароль</label>
            <Password
              id="password"
              v-model="credentials.password"
              toggleMask
              placeholder="Пароль"
              class="w-full"
              inputClass="w-full"
            />
          </div>

          <div class="flex flex-col gap-2">
            <label for="confirmPassword" class="font-medium">Подтвердите пароль</label>
            <Password
              id="confirmPassword"
              v-model="confirmPassword"
              toggleMask
              :feedback="false"
              placeholder="Повторите пароль"
              class="w-full"
              inputClass="w-full"
            />
          </div>

          <div v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</div>

          <Button
            label="Зарегистрироваться"
            :loading="loading"
            type="submit"
            class="w-full"
          />

          <div class="text-center mt-4">
            <span class="text-gray-600">Уже есть аккаунт? </span>
            <NuxtLink to="/login" class="text-blue-600 hover:underline">Войти</NuxtLink>
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>

<script setup>
definePageMeta({
  layout: false
})

import { useAuthStore } from '~/stores/auth';

const authStore = useAuthStore();
const credentials = ref({
  email: '',
  password: '',
});
const errorMessage = ref('');
const loading = ref(false);
const confirmPassword = ref('');

async function handleRegister() {
  errorMessage.value = '';

  // Проверка совпадения паролей
  if (credentials.value.password !== confirmPassword.value) {
    errorMessage.value = 'Пароли не совпадают!';
    return;
  }

  loading.value = true;
  try {
    await authStore.register(credentials.value);
    navigateTo('/profile/me');
  } catch (error) {
    errorMessage.value = 'Ошибка регистрации: ' + (error.message || 'Неверные данные!');
  } finally {
    loading.value = false;
  }
}
</script>