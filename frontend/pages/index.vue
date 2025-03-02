<template>
    <div class="landing-page">
      <!-- Hero Section -->
      <section class="hero-section py-20 text-center">
        <div class="container mx-auto px-4">
          <h1 class="text-4xl md:text-4xl font-bold mb-6">
            Лучший маркетплейс твоего города
          </h1>
          <div class="text-7xl font-extrabold text-primary mb-8">
            Рязань Маркетс
          </div>
          <p class="text-xl md:text-2xl">
            Лучшие условия для покупателей и начинающих предпринимателей
          </p>
        </div>
      </section>
  
      <!-- Преимущества -->
      <section class="py-16">
        <div class="container mx-auto">
          <h2 class="text-3xl font-bold text-center mb-12">Наши преимущества</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card class="text-center py-6 shadow-lg">
              <template #content>
                <i class="pi pi-bolt text-5xl text-primary mb-4"></i>
                <h3 class="text-xl font-bold mb-2">Мгновенная доставка</h3>
                <p class="text-gray-200">Получайте заказы в день оформления</p>
              </template>
            </Card>
  
            <Card class="text-center py-6 shadow-lg">
              <template #content>
                <i class="pi pi-shield text-5xl text-primary mb-4"></i>
                <h3 class="text-xl font-bold mb-2">Безопасность</h3>
                <p class="text-gray-200">Гарантия возврата и защита платежей</p>
              </template>
            </Card>
  
            <Card class="text-center py-6 shadow-lg">
              <template #content>
                <i class="pi pi-users text-5xl text-primary mb-4"></i>
                <h3 class="text-xl font-bold mb-2">Поддержка 24/7</h3>
                <p class="text-gray-200">Круглосуточная помощь покупателям</p>
              </template>
            </Card>
  
            <Card class="text-center py-6 shadow-lg">
              <template #content>
                <i class="pi pi-chart-line text-5xl text-primary mb-4"></i>
                <h3 class="text-xl font-bold mb-2">Для бизнеса</h3>
                <p class="text-gray-200">Минимальные комиссии для продавцов</p>
              </template>
            </Card>
          </div>
        </div>
      </section>
  
      <!-- FAQ Section -->
      <section class="py-16">
    <div class="container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-12">Частые вопросы</h2>
      <Accordion>
        <AccordionPanel v-for="(item, index) in faqItems" :key="index" :value="String(index)">
          <AccordionHeader>{{ item.header }}</AccordionHeader>
          <AccordionContent>
            <p class="m-0 text-gray-200">
              {{ item.content }}
            </p>
          </AccordionContent>
        </AccordionPanel>
      </Accordion>
    </div>
  </section>
    </div>
  </template>
  
  <script setup>
const faqItems = ref([
  {
    header: "Как начать продавать?",
    content: "Зарегистрируйтесь как продавец, заполните информацию о товарах и начинайте принимать заказы уже сегодня!"
  },
  {
    header: "Способы оплаты",
    content: "Мы принимаем банковские карты, электронные кошельки и наличные при получении"
  },
  {
    header: "Условия доставки",
    content: "Бесплатная доставка при заказе от 2000₽. Возможен самовывоз из 50+ пунктов выдачи"
  },
  {
    header: "Гарантии качества",
    content: "Все товары проходят проверку перед продажей. 14 дней на возврат без вопросов"
  }
]);
  </script>
  
  <style scoped>
  .hero-section {
    min-height: 70vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .text-primary {
    color: #2563eb;
  }
  
  .p-accordion {
    max-width: 800px;
    margin: 0 auto;
  }
  
  .p-accordion-header {
    font-size: 1.1rem;
    font-weight: 600;
  }
  
  .p-card {
    transition: transform 0.3s ease;
  }
  
  .p-card:hover {
    transform: translateY(-5px);
  }
  </style>