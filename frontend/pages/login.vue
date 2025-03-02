<template>
    <div class="min-h-screen flex flex-col items-center justify-center p-4">
      <Card class="w-full max-w-md">
        <template #title>
          <div class="text-2xl font-bold">Вход в систему</div>
        </template>
        <template #content>
          <form @submit.prevent="handleLogin" class="space-y-4">
  
            <div class="flex flex-col gap-2">
              <label for="credentials.email" class="font-medium">Email</label>
              <InputText id="credentials.email" v-model="credentials.email" type="email" placeholder="Ваш email" />
            </div>
  
            <div class="flex flex-col gap-2">
              <label for="credentials.password" class="font-medium">Пароль</label>
              <InputText id="credentials.password" toggleMask v-model="credentials.password" type="password" placeholder="Пароль" />
            </div>
  
            <div v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</div>

            <Button label="Войти" :loading="loading" type="submit" class="w-full" />
  
            <div class="text-center mt-4">
              <span class="text-gray-600">Нет аккаунта? </span>
              <NuxtLink to="/register" class="text-blue-600 hover:underline">Зарегистрироваться</NuxtLink>
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
  password: ''
});
const errorMessage = ref('');
const loading = ref(false);

async function handleLogin() {
  errorMessage.value = '';

  loading.value = true;
  try {
    await authStore.login(credentials.value);
    navigateTo('/profile/me');
  } catch (error) {
    errorMessage.value = 'Неверные данные!';
  } finally {
    loading.value = false;
  }
}
</script>