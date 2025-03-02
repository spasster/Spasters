<template>
    <div>
      <Button 
        label="Добавить товар" 
        icon="pi pi-plus" 
        @click="openModal"
        class=" w-full"
      />
  
      <Dialog 
        v-model:visible="displayModal" 
        :style="{ width: '90vw', maxWidth: '800px' }" 
        header="Создание нового товара"
        :modal="true"
      >
        <form @submit.prevent="submitProduct" class="p-fluid">
          <div class="grid gap-4">
            <!-- Основная информация -->
            <div class="col-12 md:col-6">
              <div class="field">
                <label for="title" class="font-medium">Название товара *</label>
                <InputText 
                  id="title" 
                  v-model="product.title" 
                  placeholder="Введите название"
                  class="w-full"
                />
              </div>
  
              <div class="field mt-4">
                <label for="price" class="font-medium">Цена *</label>
                <InputNumber 
                  id="price" 
                  v-model="product.price" 
                  mode="currency" 
                  currency="RUB" 
                  locale="ru-RU"
                  class="w-full"
                />
              </div>
  
              <div class="field mt-4">
                <label for="type" class="font-medium">Тип товара *</label>
                <Dropdown 
                  id="type"
                  v-model="product.type"
                  :options="productTypes"
                  optionLabel="name"
                  placeholder="Выберите тип"
                  class="w-full"
                />
              </div>
  
              <div class="field mt-4">
                <label for="category" class="font-medium">Категория *</label>
                <Dropdown 
                  id="category"
                  v-model="product.category"
                  :options="categories"
                  optionLabel="name"
                  placeholder="Выберите категорию"
                  class="w-full"
                />
              </div>
            </div>
  
            <!-- Описание и фото -->
            <div class="col-12 md:col-6">
              <div class="field">
                <label for="description" class="font-medium">Описание</label>
                <Textarea 
                  id="description" 
                  v-model="product.description" 
                  rows="5" 
                  autoResize
                  placeholder="Подробное описание товара"
                  class="w-full"
                />
              </div>
  
              <div class="field mt-4">
                <label class="font-medium">Фотографии товара *</label>
                <FileUpload 
                  name="photos[]"
                  :multiple="true"
                  accept="image/*"
                  :maxFileSize="2000000"
                  chooseLabel="Загрузить фото"
                  @select="handleUpload"
                  :showUploadButton="false"
                  :showCancelButton="false"
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
                          :src="photo.photo" 
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
                <small class="text-gray-500">Максимум 5 фото, до 2MB каждая</small>
              </div>
            </div>
          </div>
  
          <div class="flex justify-between mt-6">
            <Button 
              label="Отмена" 
              icon="pi pi-times" 
              class="p-button-text"
              @click="closeModal"
            />
            <Button 
              type="submit" 
              label="Создать товар" 
              icon="pi pi-check" 
              :loading="loading"
            />
          </div>
  
          <div v-if="errorMessage" class="text-red-500 mt-3">{{ errorMessage }}</div>
        </form>
      </Dialog>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const { $apiFetch } = useNuxtApp()

  const displayModal = ref(false);
  const loading = ref(false);
  const errorMessage = ref('');
  
  const product = ref({
    title: '',
    price: 0,
    type: null,
    category: null,
    description: '',
    photos: []
  });
  
  const productTypes = ref([
    { name: 'Продукт', value: 'product' },
    { name: 'Услуга', value: 'service' }
  ]);
  
  const categories = ref([
    { name: 'Техника', value: 'Mobile Phones' },
    { name: 'Свечи', value: 'Laptops' }
  ]);
  
  const openModal = () => {
    displayModal.value = true;
  };
  
  const closeModal = () => {
    displayModal.value = false;
    resetForm();
  };
  
  const resetForm = () => {
    product.value = {
      title: '',
      price: 0,
      type: null,
      category: null,
      description: '',
      photos: []
    };
    errorMessage.value = '';
  };
  
  const handleUpload = async (event) => {
    const files = event.files;
    if (product.value.photos.length + files.length > 5) {
      errorMessage.value = 'Можно загрузить не более 5 фото';
      return;
    }
  
    for (const file of files) {
      const reader = new FileReader();
      reader.onload = (e) => {
        product.value.photos.push({
          photo: e.target.result
        });
      };
      reader.readAsDataURL(file);
    }
  };
  
  const removePhoto = (index) => {
    product.value.photos.splice(index, 1);
  };
  
  const submitProduct = async () => {
    errorMessage.value = '';
    
    // Валидация
    if (!product.value.title.trim()) {
      errorMessage.value = 'Введите название товара';
      return;
    }
    if (product.value.price <= 0) {
      errorMessage.value = 'Укажите корректную цену';
      return;
    }
    if (!product.value.type) {
      errorMessage.value = 'Выберите тип товара';
      return;
    }
    product.value.type = product.value.type.value
    if (!product.value.category) {
      errorMessage.value = 'Выберите категорию';
      return;
    }
    product.value.category = product.value.category.name

    if (product.value.photos.length === 0) {
      errorMessage.value = 'Добавьте хотя бы одно фото';
      return;
    }
  
    try {
      loading.value = true;
      // Здесь API запрос на создание товара
      console.log('Отправка данных:', JSON.parse(JSON.stringify(product.value)));
      await $apiFetch('/api/products/create_product/', {
        method: 'POST',
        body: JSON.stringify(product.value)
        });
      
      // После успешного создания
      closeModal();
    } catch (error) {
      errorMessage.value = 'Ошибка при создании товара: ' + error.message;
    } finally {
      loading.value = false;
    }
  };
  </script>
  
  <style scoped>
  .field label {
    display: block;
    margin-bottom: 0.5rem;
  }
  
  .p-fileupload-content {
    border: 2px dashed #ccc;
    padding: 1rem;
    border-radius: 8px;
    transition: border-color 0.3s;
  }
  
  .p-fileupload-content:hover {
    border-color: #3B82F6;
  }

.grid {
    flex-direction: column;
}

.col-12 {
    width: 100%;
    padding: 0;
}
  
  </style>