<template>
    <div class="card">
        <DataView :value="filteredProducts" :sortOrder="sortOrder" :sortField="sortField" :layout="layout" :paginator="true" :rows="rowsPerPage" :totalRecords="totalRecords">
            <template #header>
                <div class="flex flex-column md:flex-row md:justify-content-between gap-4 mb-4">
                    <div class="flex flex-wrap gap-4">
                        <Select v-model="sortKey" :options="sortOptions" optionLabel="label" placeholder="Сортировать по цене" @change="onSortChange($event)" />
                    </div>
                    <div class="flex gap-4">
                        <SelectButton v-model="layout" :options="layoutOptions" :allowEmpty="false">
                            <template #option="{ option }">
                                <i :class="[option === 'list' ? 'pi pi-bars' : 'pi pi-table']" />
                            </template>
                        </SelectButton>
                    </div>
                </div>
            </template>

            <template #list="slotProps">
                <div class="flex flex-col">
                    <div v-for="(item, index) in slotProps.items" class="cursor-pointer" :key="index" @click="navigateToProduct(item.id)">
                        <div class="flex flex-col sm:flex-row sm:items-center p-6 gap-4 border border-surface-200 dark:border-surface-700"
                        :class="{ 'border-t border-surface-200 dark:border-surface-700': index !== 0 }">
                            <div class="md:w-40 relative">
                                <img class="rounded w-full object-cover h-32" :src="item.image" :alt="item.name" />
                                <Tag :value="item.inventoryStatus" :severity="getSeverity(item)"
                                    class="absolute left-2 top-2" />
                            </div>
                            <div class="flex-1 flex flex-col md:flex-row justify-between gap-6">
                                <div>
                                    <span class="text-surface-500 text-sm">{{ item.category }}</span>
                                    <div class="text-lg font-medium mt-2">{{ item.name }}</div>
                                </div>
                                <div class="flex flex-col md:items-end gap-8">
                                    <span class="text-xl font-semibold">₽{{ item.price.toLocaleString() }}</span>
                                    <div class="flex gap-2">
                                        <Button icon="pi pi-heart" outlined />
                                        <Button icon="pi pi-shopping-cart" label="Купить"
                                            :disabled="item.inventoryStatus === 'OUTOFSTOCK'"
                                            class="bg-primary-500 hover:bg-primary-600" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #grid="slotProps">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div v-for="(item, index) in slotProps.items" :key="index"
                        class="p-4 rounded-lg bg-surface-50 cursor-pointer" @click="navigateToProduct(item.id)">
                        <div class="relative mb-4">
                            <img class="rounded-lg w-full object-cover h-64" :src="item.image" :alt="item.name" />
                            <Tag :value="item.inventoryStatus" :severity="getSeverity(item)"
                                class="absolute left-2 top-2" />
                        </div>
                        <div class="flex flex-col gap-3">
                            <div>
                                <span class="text-surface-500 text-sm">{{ item.category }}</span>
                                <div class="text-lg font-medium mt-1">{{ item.name }}</div>
                            </div>
                            <div class="flex justify-between items-center">
                                <span class="text-xl font-semibold">₽{{ item.price.toLocaleString() }}</span>
                                <div class="flex items-center gap-2 bg-surface-100 px-3 py-1 rounded-full">
                                    <i class="pi pi-star-fill text-yellow-500"></i>
                                    <span>{{ item.rating }}</span>
                                </div>
                            </div>
                            <div class="flex gap-2 mt-2">
                                <Button icon="pi pi-shopping-cart" label="Купить" class="flex-1"
                                    :disabled="item.inventoryStatus === 'OUTOFSTOCK'" />
                                <Button icon="pi pi-heart" outlined />
                            </div>
                        </div>
                    </div>
                </div>
            </template>

            <template #paginatorstart>
                <span class="text-surface-500">Показано {{ filteredProducts.length }} из {{ totalRecords }} товаров</span>
            </template>
        </DataView>
    </div>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue';
const route = useRoute()


// Получаем продукты через пропс
const props = defineProps({
  products: {
    type: Array,
    required: true
  }
});

const sortKey = ref();
const sortOrder = ref();
const sortField = ref();
const sortOptions = ref([
    {label: 'От большей к меньшей', value: '!price'},
    {label: 'От меньшей к большей', value: 'price'},
]);

const navigateToProduct = (id) => {
  // Находим продукт по ID из пропсов
  const product = props.products.find(item => item.id === id);
  
  // Если продукт найден, извлекаем type и category
  if (product) {
    const { type, category } = product;
    navigateTo(`/products/${type}/${category}/${id}`);
  } else {
    console.error("Product not found");
  }
};

const onSortChange = (event) => {
    const value = event.value.value;
    const sortValue = event.value;

    if (value.indexOf('!') === 0) {
        sortOrder.value = -1;
        sortField.value = value.substring(1, value.length);
        sortKey.value = sortValue;
    }
    else {
        sortOrder.value = 1;
        sortField.value = value;
        sortKey.value = sortValue;
    }
};

const layout = ref('grid');
const layoutOptions = ref(['list', 'grid']);
const rowsPerPage = ref(6);
const totalRecords = computed(() => filteredProducts.value.length);

// Фильтры
const selectedCategory = ref(null);
const selectedStatus = ref(null);

const categories = ref([
    { name: 'Все категории', code: null },
    { name: 'Смартфоны', code: 'Смартфоны' },
    { name: 'Ноутбуки', code: 'Ноутбуки' },
    { name: 'Наушники', code: 'Наушники' }
]);

const statuses = ref([
    { label: 'Все статусы', value: null },
    { label: 'В наличии', value: 'INSTOCK' },
    { label: 'Мало на складе', value: 'LOWSTOCK' },
    { label: 'Нет в наличии', value: 'OUTOFSTOCK' }
]);

const filteredProducts = computed(() => {
    return props.products.filter(product => {
        const categoryMatch = !selectedCategory.value?.code || 
                            product.category === selectedCategory.value.code;
        const statusMatch = !selectedStatus.value?.value || 
                          product.inventoryStatus === selectedStatus.value.value;
        return categoryMatch && statusMatch;
    });
});

const getSeverity = (product) => {
    switch (product.inventoryStatus) {
        case 'INSTOCK': return 'success';
        case 'LOWSTOCK': return 'warning';
        case 'OUTOFSTOCK': return 'danger';
        default: return null;
    }
};
</script>

<style scoped>
.card {
    background: var(--surface-card);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.p-dropdown {
    width: 100%;
    max-width: 240px;
}

@media (max-width: 640px) {
    .grid {
        grid-template-columns: 1fr;
    }
    
    .flex-row {
        flex-direction: column;
        gap: 1rem;
    }
}

.bg-primary-500 {
    background-color: var(--primary-500);
}

.bg-primary-500:hover {
    background-color: var(--primary-600);
}
</style>
