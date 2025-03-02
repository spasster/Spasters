<template>
    <Cart />
  </template>
  
  <script setup>
  import { useCartStore } from '@/stores/cart';
  
  const cart = useCartStore();
  
  const product = {
    id: 1,
    name: 'Xiaomi Redmi Note 12',
    price: 25990,
    category: 'Смартфоны',
    image: '/images/redmi-note12.jpg'
  };
  
  const addToCart = () => {
    cart.addItem(product);
  };
  </script>