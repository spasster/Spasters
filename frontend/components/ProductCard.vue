<template>
    <Card class="h-full shadow-lg hover:shadow-xl transition-shadow duration-300">
      <template #header>
        <div class="relative">
          <Carousel 
            v-if="product.photos?.length"
            :value="product.photos" 
            :numVisible="1" 
            :numScroll="1" 
            circular
            class=""
          >
            <template #item="slotProps">
              <img 
                :src="slotProps.data.photo" 
                :alt="product.title"
                class="w-full h-64 object-cover"
              />
            </template>
          </Carousel>
          <Tag 
            :value="product.active ? 'В продаже' : 'Недоступно'"
            :severity="product.active ? 'success' : 'danger'"
            class="absolute top-2 left-2"
          />
        </div>
      </template>
  
      <template #title>
        <div class="flex justify-between items-start">
          <span class="truncate">{{ product.title }}</span>
          <div class="flex gap-2">
            <Tag :value="product.type" severity="info" />
            <Tag :value="product.category" severity="warning" />
          </div>
        </div>
      </template>
  
      <template #content>
        <p class="line-clamp-3 text-gray-600 dark:text-gray-300 mb-4">
          {{ product.description }}
        </p>
        
        <div class="flex items-center justify-between mt-4">
          <span class="text-2xl font-bold text-primary">
            {{ formatPrice(product.price) }} ₽
          </span>
          <div class="flex gap-2">
            <Button 
              icon="pi pi-heart" 
              outlined 
              class="p-button-rounded p-button-sm"
            />
            <Button 
              icon="pi pi-shopping-cart" 
              class=" p-button-rounded p-button-sm"
              :disabled="!product.active"
            />
          </div>
        </div>
      </template>
    </Card>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  const props = defineProps({
    product: {
      type: Object,
      required: true,
      default: () => ({
        title: '',
        price: 0,
        type: '',
        category: '',
        description: '',
        active: false,
        photos: []
      })
    }
  });
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('ru-RU').format(price);
  };
  </script>
  
  <style scoped>

  </style>