import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem('cart')) || []);

  // Геттеры
  const cartItems = computed(() => items.value);
  const cartTotal = computed(() => 
    items.value.reduce((total, item) => total + item.price * item.quantity, 0)
  );

  // Действия
  function addItem(product) {
    const existingItem = items.value.find(item => item.id === product.id);
    
    if (existingItem) {
      existingItem.quantity++;
    } else {
      items.value.push({
        ...product,
        quantity: 1
      });
    }
    saveToLocalStorage();
  }

  function updateQuantity(productId, quantity) {
    const item = items.value.find(item => item.id === productId);
    if (item) {
      item.quantity = Math.max(1, quantity);
      saveToLocalStorage();
    }
  }

  function removeItem(productId) {
    items.value = items.value.filter(item => item.id !== productId);
    saveToLocalStorage();
  }

  function clearCart() {
    items.value = [];
    saveToLocalStorage();
  }

  function saveToLocalStorage() {
    localStorage.setItem('cart', JSON.stringify(items.value));
  }

  return {
    items,
    cartItems,
    cartTotal,
    addItem,
    updateQuantity,
    removeItem,
    clearCart
  };
});