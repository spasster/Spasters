<template>
    <div class="container mx-auto p-4 min-h-screen">
      <div class="max-w-3xl mx-auto rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between mb-8">
          <h1 class="text-2xl font-bold">Создание нового товара</h1>
          <Button 
            label="Вернуться назад" 
            icon="pi pi-arrow-left" 
            class="p-button-text"
            @click="$router.go(-1)"
          />
        </div>
  
        <form @submit.prevent="submitProduct" class="space-y-6">
          <!-- Основная информация -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Левая колонка -->
            <div class="space-y-4">
              <div class="field">
                <label class="block text-sm font-medium mb-2">Название товара *</label>
                <InputText
                  v-model.trim="product.title"
                  placeholder="iPhone 15 Pro Max"
                  :class="{ 'p-invalid': errors.title }"
                  class="w-full"
                />
                <small v-if="errors.title" class="p-error">{{ errors.title }}</small>
              </div>
  
              <div class="field">
                <label class="block text-sm font-medium mb-2">Цена (₽) *</label>
                <InputNumber
                  v-model="product.price"
                  mode="currency"
                  currency="RUB"
                  locale="ru-RU"
                  :class="{ 'p-invalid': errors.price }"
                  class="w-full"
                />
                <small v-if="errors.price" class="p-error">{{ errors.price }}</small>
              </div>
  
              <div class="field">
                <label class="block text-sm font-medium mb-2">Тип товара *</label>
                <Dropdown
                  v-model="product.type"
                  :options="productTypes"
                  optionLabel="name"
                  placeholder="Выберите тип"
                  :class="{ 'p-invalid': errors.type }"
                  class="w-full"
                />
                <small v-if="errors.type" class="p-error">{{ errors.type }}</small>
              </div>
  
              <div class="field">
                <label class="block text-sm font-medium mb-2">Категория *</label>
                <div class="flex gap-2">
                  <AutoComplete
                    v-model="selectedCategory"
                    :suggestions="filteredCategories"
                    @complete="searchCategory"
                    field="name"
                    placeholder="Ноутбуки"
                    :class="{ 'p-invalid': errors.category }"
                    class="flex-1"
                  />
                  <Button 
                    icon="pi pi-plus" 
                    class="p-button-outlined"
                    @click="addCustomCategory"
                    v-tooltip="'Добавить новую категорию'"
                  />
                </div>
                <small v-if="errors.category" class="p-error">{{ errors.category }}</small>
              </div>
            </div>
  
            <!-- Правая колонка -->
            <div class="space-y-4">
              <div class="field">
                <label class="block text-sm font-medium mb-2">Описание</label>
                <Textarea
                  v-model.trim="product.description"
                  rows="5"
                  autoResize
                  placeholder="Опишите особенности товара..."
                  class="w-full"
                />
              </div>
  
              <div class="field">
                <label class="block text-sm font-medium mb-2">Фотографии товара *</label>
                <FileUpload
                  name="photos[]"
                  :multiple="true"
                  accept="image/*"
                  :maxFileSize="2000000"
                  chooseLabel="Выбрать файлы"
                  :class="{ 'p-invalid': errors.photos }"
                  @select="handleUpload"
                  :showUploadButton="false"
                  class="w-full"
                >
                  <template #content>
                    <div v-if="product.photos.length" class="flex flex-wrap gap-2 mt-2">
                      <div 
                        v-for="(photo, index) in product.photos" 
                        :key="index"
                        class="relative w-24 h-24 border-round"
                      >
                        <img 
                          :src="photo.preview" 
                          :alt="`Preview ${index}`"
                          class="w-full h-full border-round object-cover"
                        />
                        <Button 
                          icon="pi pi-times" 
                          @click="removePhoto(index)"
                          class="p-button-danger p-button-sm absolute top-0 right-0"
                        />
                      </div>
                    </div>
                  </template>
                </FileUpload>
                <small v-if="errors.photos" class="p-error">{{ errors.photos }}</small>
                <small class="text-gray-500">Максимум 5 фото, до 2MB каждая</small>
              </div>
            </div>
          </div>
  
          <Divider />
  
          <div class="flex justify-end gap-4">
            <Button
              type="button"
              label="Очистить форму"
              icon="pi pi-trash"
              class="p-button-danger"
              @click="resetForm"
            />
            <Button
              type="submit"
              label="Создать товар"
              icon="pi pi-check"
              :loading="loading"
              class="p-button-success"
            />
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useToast } from 'primevue/usetoast';
  import { useRouter } from 'vue-router';

  const { $apiFetch } = useNuxtApp()

  
  const toast = useToast();
  const router = useRouter();
  
  // Состояния формы
  const loading = ref(false);
  const selectedCategory = ref('');
  const customCategories = ref([]);
  
  const product = ref({
    title: '',
    price: 0,
    type: null,
    category: '',
    description: '',
    photos: []
  });
  
  // Ошибки валидации
  const errors = ref({
    title: '',
    price: '',
    type: '',
    category: '',
    photos: ''
  });
  
  // Справочники
  const productTypes = ref([
    { name: 'Электроника', value: 'electronics' },
    { name: 'Одежда', value: 'clothing' },
    { name: 'Мебель', value: 'furniture' }
  ]);
  
  const categories = ref([
    'Смартфоны',
    'Ноутбуки',
    'Планшеты',
    'Аксессуары',
    'Одежда',
    'Обувь'
  ]);
  
  // Фильтрация категорий
  const filteredCategories = ref([]);
  const searchCategory = (event) => {
    const query = event.query.toLowerCase();
    filteredCategories.value = categories.value.filter(cat => 
      cat.toLowerCase().includes(query)
    );
  };
  
  // Добавление кастомной категории
  const addCustomCategory = () => {
    if (selectedCategory.value && !customCategories.value.includes(selectedCategory.value)) {
      customCategories.value.push(selectedCategory.value);
      selectedCategory.value = '';
    }
  };
  
  // Удаление кастомной категории
  const removeCustomCategory = (index) => {
    customCategories.value.splice(index, 1);
  };
  
  // Обработка загрузки фото
  const handleUpload = async (event) => {
    const files = event.files;
    if (product.value.photos.length + files.length > 5) {
      showError('Можно загрузить не более 5 фото');
      return;
    }
  
    for (const file of files) {
      const reader = new FileReader();
      reader.onload = (e) => {
        product.value.photos.push({
          file,
          preview: e.target.result
        });
      };
      reader.readAsDataURL(file);
    }
  };
  
  // Удаление фото
  const removePhoto = (index) => {
    product.value.photos.splice(index, 1);
  };
  
  // Валидация формы
  const validateForm = () => {
    errors.value = { title: '', price: '', type: '', category: '', photos: '' };
    let isValid = true;
  
    if (!product.value.title.trim()) {
      errors.value.title = 'Введите название товара';
      isValid = false;
    }
  
    if (product.value.price <= 0) {
      errors.value.price = 'Укажите корректную цену';
      isValid = false;
    }
  
    if (!product.value.type) {
      errors.value.type = 'Выберите тип товара';
      isValid = false;
    }
  
    if (customCategories.value.length === 0 && !selectedCategory.value) {
      errors.value.category = 'Укажите хотя бы одну категорию';
      isValid = false;
    }
  
    if (product.value.photos.length === 0) {
      errors.value.photos = 'Добавьте хотя бы одно фото';
      isValid = false;
    }
  
    return isValid;
  };
  
  // Отправка формы
  const submitProduct = async () => {
    if (!validateForm()) return;
  
    try {
      loading.value = true;
      await $apiFetch('/api/products/create_product/', {
        method: 'POST',
        body: product.value
      });
  
      toast.add({ severity: 'success', summary: 'Товар создан успешно' });
    } catch (err) {
      toast.add({ severity: 'error', summary: 'Ошибка при создании товара', detail: err.message });
    } finally {
      loading.value = false;
    }
  };
  
  // Сброс формы
  const resetForm = () => {
    product.value = {
      title: '',
      price: 0,
      type: null,
      category: '',
      description: '',
      photos: []
    };
  };
  </script>
  