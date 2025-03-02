<template>
    <footer class="bg-gray-900 text-gray-300 py-12 mt-20">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
          <!-- Контакты -->
          <div class="space-y-4">
            <h3 class="text-xl font-bold text-white mb-4">Контакты</h3>
            <div class="flex items-center gap-2">
              <i class="pi pi-phone text-primary"></i>
              <a href="tel:+78005553535" class="text-lg hover:text-primary transition-colors">
                8 (800) 555-35-35
              </a>
            </div>
            <p class="text-sm">Круглосуточная горячая линия</p>
            <div class="flex items-center gap-2 mt-4">
              <i class="pi pi-envelope text-primary"></i>
              <a href="mailto:info@marketplace.ru" class="hover:text-primary transition-colors">
                info@marketplace.ru
              </a>
            </div>
          </div>
  
          <!-- Полезные ссылки -->
          <div>
            <h3 class="text-xl font-bold text-white mb-4">Покупателям</h3>
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-primary transition-colors">Доставка</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Оплата</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Возврат</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Помощь</a></li>
            </ul>
          </div>
  
          <!-- Правовая информация -->
          <div>
            <h3 class="text-xl font-bold text-white mb-4">Информация</h3>
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-primary transition-colors">О компании</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Вакансии</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Партнерам</a></li>
              <li><a href="#" class="hover:text-primary transition-colors">Реквизиты</a></li>
            </ul>
          </div>
  
          <!-- Соцсети -->
          <div>
            <h3 class="text-xl font-bold text-white mb-4">Мы в соцсетях</h3>
            <div class="flex gap-4">
              <a href="#" class="social-icon">
                <i class="pi pi-facebook"></i>
              </a>
              <a href="#" class="social-icon">
                <i class="pi pi-telegram"></i>
              </a>
              <a href="#" class="social-icon">
                <i class="pi pi-instagram"></i>
              </a>
              <a href="#" class="social-icon">
                <i class="pi pi-youtube"></i>
              </a>
            </div>
          </div>
        </div>
  
        <!-- Нижняя панель -->
        <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="text-center md:text-left">
            <p class="text-sm">&copy; 2024 Рязань Маркетс. Все права защищены</p>
          </div>
          <div class="flex gap-6">
            <a href="#" class="text-sm hover:text-primary transition-colors">Политика конфиденциальности</a>
            <a href="#" class="text-sm hover:text-primary transition-colors">Пользовательское соглашение</a>
          </div>
        </div>
      </div>
    </footer>
  </template>
  
  <style scoped>
  .social-icon {
    @apply w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center 
           text-xl  transition-colors duration-300;
  }
  
  .text-primary {
    color: #3b82f6; /* Синий цвет, можно изменить */
  }
  </style>