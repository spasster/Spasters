
<template>
  <div class="">
    <MegaMenu :model="items">
      <template #start>
        <NuxtLink 
          to="/" 
          class="flex items-center gap-2 no-underline text-color hover:text-primary transition-colors"
        >
          <i class="pi pi-home" />
          <span class="font-medium">Главная</span>
        </NuxtLink>
      </template>

      <template #end>
        <div class="flex items-center gap-4">
            <ThemeChange /> <!-- Ваш существующий компонент -->

            <OverlayBadge v-if="cart.items.length > 0" :value="cart.items.length" severity="danger" position="top-right">
                <Button icon="pi pi-shopping-cart" class="p-button-rounded p-button-outlined" @click="navigateTo('/cart')" />
            </OverlayBadge>

            <div v-if="authStore.accessToken">
              <Avatar
                v-if="authStore.user.avatar"
                 class="cursor-pointer"
                 :image="authStore.user.avatar"
                 shape="circle" 
                 @click="navigateTo('/profile/me')"
              />
              <Avatar
                v-else
                 class="cursor-pointer"
                 :image="authStore.user.avatar ||'/user.png'"
                 shape="circle" 
                 @click="navigateTo('/profile/me')"
              />
            </div>
             
            <NuxtLink to="/login" v-else>
                <Button 
                    label="Войти"
                    icon="pi pi-user"
                    class="p-button-text p-button-rounded"
                />
            </NuxtLink>
            
          
        </div>
      </template>
    </MegaMenu>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from '~/stores/auth';
import { navigateTo } from '#app';

const authStore = useAuthStore();
const cart = useCartStore();


const items = ref([
  {
    label: 'Продукты',
    icon: 'pi pi-shopping-bag',
    items: [
      [
        {
          label: 'Категории',
          items: [
            { 
              label: 'Техника', 
              command: () => navigateTo('/products/product/Техника'),
            },
            { 
              label: 'Свечи', 
              command: () => navigateTo('/products/product/Свечи'),
            }
          ]
        }
      ]
    ]
  },
  {
    label: 'Услуги',
    icon: 'pi pi-wrench',
    items: [
      [
        {
        label: 'Категории',
          items: [
            { 
              label: 'Свечи', 
              command: () => navigateTo('/products/service/Свечи'),
            }
          ]
        }
      ]
    ]
  }
]);

// Обработчик для команд меню
const handleCommand = (command) => {
  if (typeof command === 'function') {
    command();
  }
};
</script>
