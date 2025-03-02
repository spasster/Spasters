<template>
    <div>
      <Button 
        label="Верифицироваться как продавец" 
        @click="showDialog = true"
        class="bg-blue-500 hover:bg-blue-600 text-white"
        :disabled="isVerified"
      />
  
      <Dialog 
        v-model:visible="showDialog" 
        modal
        header="Верификация продавца"
        :style="{ width: '600px' }"
      >
        <div class="flex flex-col gap-4">
          <div class="grid grid-cols-3 gap-4">
            <div class="flex flex-col gap-2">
              <label class="font-medium">Фамилия*</label>
              <InputText 
                v-model="formData.surname" 
                :class="{ 'p-invalid': errors.surname }"
              />
              <small v-if="errors.surname" class="text-red-500">Обязательное поле</small>
            </div>
            
            <div class="flex flex-col gap-2">
              <label class="font-medium">Имя*</label>
              <InputText 
                v-model="formData.name" 
                :class="{ 'p-invalid': errors.name }"
              />
              <small v-if="errors.name" class="text-red-500">Обязательное поле</small>
            </div>
  
            <div class="flex flex-col gap-2">
              <label class="font-medium">Отчество*</label>
              <InputText 
                v-model="formData.patronymic" 
                :class="{ 'p-invalid': errors.patronymic }"
              />
              <small v-if="errors.patronymic" class="text-red-500">Обязательное поле</small>
            </div>
          </div>
  
          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-2">
              <label class="font-medium">Дата рождения*</label>
              <Calendar 
                v-model="formData.birthdate" 
                dateFormat="dd.mm.yy"
                showIcon
                :class="{ 'p-invalid': errors.birthdate }"
                :maxDate="maxBirthDate"
              />
              <small v-if="errors.birthdate" class="text-red-500">Неверная дата</small>
            </div>
  
            <div class="flex flex-col gap-2">
              <label class="font-medium">ИНН*</label>
              <InputNumber 
                v-model="formData.inn" 
                :maxlength="12"
                :min="0"
                class="w-full"
                :class="{ 'p-invalid': errors.inn }"
              />
              <small v-if="errors.inn" class="text-red-500">12 цифр</small>
            </div>
          </div>
  
          <div class="grid grid-cols-2 gap-4">
            <div class="flex flex-col gap-2">
              <label class="font-medium">Номер документа*</label>
              <InputMask
                v-model="formData.docnumber"
                mask="99 99 999999"
                placeholder="__ __ ______"
                class="w-full"
                :class="{ 'p-invalid': errors.docnumber }"
              />
              <small v-if="errors.docnumber" class="text-red-500">Неверный формат</small>
            </div>
  
            <div class="flex flex-col gap-2">
              <label class="font-medium">Дата выдачи*</label>
              <Calendar 
                v-model="formData.docdate" 
                dateFormat="dd.mm.yy"
                showIcon
                :class="{ 'p-invalid': errors.docdate }"
                :maxDate="new Date()"
              />
              <small v-if="errors.docdate" class="text-red-500">Неверная дата</small>
            </div>
          </div>
  
          <div class="flex justify-end gap-2 mt-4">
            <Button 
              label="Отмена" 
              severity="secondary"
              :disabled="isSubmitting"
              @click="resetForm"
            />
            <Button 
              label="Отправить" 
              severity="primary"
              :loading="isSubmitting"
              :disabled="!isFormValid"
              @click="handleSubmit"
            />
          </div>
  
          <div v-if="errorMessage" class="text-red-500 text-sm text-center">
            {{ errorMessage }}
          </div>
        </div>
      </Dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue';
  import { useNuxtApp } from '#app';
  import { useAuthStore } from '~/stores/auth';
  
  const { $apiFetch } = useNuxtApp();
  const authStore = useAuthStore();
  const showDialog = ref(false);
  const isSubmitting = ref(false);
  const errorMessage = ref('');
  const maxBirthDate = new Date();
  maxBirthDate.setFullYear(maxBirthDate.getFullYear() - 16);
  
  const formData = ref({
    surname: '',
    name: '',
    patronymic: '',
    birthdate: null,
    docnumber: '',
    docdate: null,
    inn: null
  });
  
  const errors = ref({
    surname: false,
    name: false,
    patronymic: false,
    birthdate: false,
    docnumber: false,
    docdate: false,
    inn: false
  });
  
  const isVerified = computed(() => authStore.user?.is_verified);
  
  const isFormValid = computed(() => {
    return Object.values(errors.value).every(error => !error) &&
      formData.value.surname.trim() &&
      formData.value.name.trim() &&
      formData.value.patronymic.trim() &&
      formData.value.birthdate &&
      formData.value.docnumber.length === 12 &&
      formData.value.docdate &&
      formData.value.inn?.toString().length === 12;
  });
  
  watch(formData, (newVal) => {
    errors.value.surname = !newVal.surname.trim();
    errors.value.name = !newVal.name.trim();
    errors.value.patronymic = !newVal.patronymic.trim();
    errors.value.birthdate = !newVal.birthdate;
    errors.value.docnumber = newVal.docnumber.length !== 12;
    errors.value.docdate = !newVal.docdate;
    errors.value.inn = newVal.inn?.toString().length !== 12;
  }, { deep: true });
  
  const resetForm = () => {
    formData.value = {
      surname: '',
      name: '',
      patronymic: '',
      birthdate: null,
      docnumber: '',
      docdate: null,
      inn: null
    };
    errors.value = {
      surname: false,
      name: false,
      patronymic: false,
      birthdate: false,
      docnumber: false,
      docdate: false,
      inn: false
    };
    showDialog.value = false;
    errorMessage.value = '';
  };
  
  const formatDate = (date) => {
    if (!date) return '';
    const d = new Date(date);
    return [
      d.getDate().toString().padStart(2, '0'),
      (d.getMonth() + 1).toString().padStart(2, '0'),
      d.getFullYear()
    ].join('.');
  };
  
  const handleSubmit = async () => {
    try {
      isSubmitting.value = true;
      errorMessage.value = '';
  
      const payload = {
        surname: formData.value.surname.trim(),
        name: formData.value.name.trim(),
        patronymic: formData.value.patronymic.trim(),
        birthdate: formatDate(formData.value.birthdate),
        docnumber: formData.value.docnumber,
        docdate: formatDate(formData.value.docdate),
        inn: formData.value.inn.toString()
      };
  
      const response = await $apiFetch('/api/auth/check_inn/', {
        method: 'POST',
        body: payload,
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      if (response.success) {
        await authStore.fetchUser();
        useToast().add({
          severity: 'success',
          summary: 'Успешно!',
          detail: 'Данные отправлены на проверку',
          life: 5000
        });
        resetForm();
      }
    } catch (error) {
      errorMessage.value = error.data?.message || 'Ошибка сервера';
      useToast().add({
        severity: 'error',
        summary: 'Ошибка!',
        detail: error.data?.message || 'Попробуйте позже',
        life: 5000
      });
    } finally {
      isSubmitting.value = false;
    }
  };
  </script>
  
  <style scoped>
  .p-invalid {
    border-color: #f87171 !important;
  }
  </style>