<template>
    <div class="min-h-screen">
      <div class="max-w-6xl mx-auto rounded-lg py-6">
        <!-- Breadcrumbs -->
        <Breadcrumb :model="breadcrumbs"/>
  
        <!-- Loading state -->
        <div v-if="isLoading" class="text-center py-8">
          <ProgressSpinner style="width: 50px; height: 50px"/>
        </div>
  
        <!-- Content -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8 pt-4">
          <!-- Image gallery -->
          <div class="space-y-4">
            <Galleria :value="product.photos" :numVisible="5" containerStyle="max-width: 100%">
              <template #item="slotProps">
                <img 
                  :src="slotProps.item.photo" 
                  :alt="product.title"
                  class="w-full h-96 object-contain rounded-lg"
                />
              </template>
              <template #thumbnail="slotProps">
                <img 
                  :src="slotProps.item.photo" 
                  :alt="product.title"
                  class="w-20 h-20 object-cover rounded cursor-pointer"
                />
              </template>
            </Galleria>
          </div>
  
          <!-- Product info -->
          <div class="space-y-6">
            <div>
              <h1 class="text-3xl font-bold">{{ product.title }}</h1>
              <div class="mt-2 flex items-center space-x-4">
                <span class="text-2xl font-semibold text-primary">
                  {{ formatPrice(product.price) }}
                </span>
                <Tag :value="product.category" class="text-sm" />
              </div>
            </div>
  
            <div class="space-y-4">
              <div class="flex items-center space-x-2">
                <i class="pi pi-tag"></i>
                <span class="">{{ product.type }}</span>
              </div>
              
              <Divider />
  
              <p class="leading-relaxed">
                {{ product.description }}
              </p>
  
              <Divider />
  
              <div class="flex space-x-4">
                <Button 
                  label="Добавить в корзину" 
                  icon="pi pi-shopping-cart" 
                  severity="warning"
                  size="large"
                  class="flex-1"
                  @click="addToCart"
                />
                <Button 
                  icon="pi pi-heart" 
                  severity="secondary"
                  outlined
                  size="large"
                />
                
    <div class="card flex justify-center">
        <Button type="button" severity="secondary"
        outlined icon="pi pi-share-alt" label="Share" @click="toggle" />

        <Popover ref="op">
            <div class="flex flex-col gap-4 w-[25rem]">
                <div>
                    <span class="font-medium block mb-2">Share this document</span>
                    <InputGroup>
                        <InputText :value="useRequestURL().href" readonly class="w-[25rem]"></InputText>
                        <InputGroupAddon>
                            <i class="pi pi-copy"></i>
                        </InputGroupAddon>
                    </InputGroup>
                </div>
                <div>
                    <span class="font-medium block mb-2">Invite Member</span>
                    <InputGroup>
                        <InputText disabled />
                        <Button label="Invite" icon="pi pi-users"></Button>
                    </InputGroup>
                </div>
                <div>
                    <span class="font-medium block mb-2">Team Members</span>
                    <ul class="list-none p-0 m-0 flex flex-col gap-4">
                        <li v-for="member in members" :key="member.name" class="flex items-center gap-2">
                            <img :src="`https://primefaces.org/cdn/primevue/images/avatar/${member.image}`" style="width: 32px" />
                            <div>
                                <span class="font-medium">{{ member.name }}</span>
                                <div class="text-sm text-surface-500 dark:text-surface-400">{{ member.email }}</div>
                            </div>
                            <div class="flex items-center gap-2 text-surface-500 dark:text-surface-400 ml-auto text-sm">
                                <span>{{ member.role }}</span>
                                <i class="pi pi-angle-down"></i>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </Popover>
    </div>


              </div>
            </div>
  
            <!-- Seller Info -->
            <div class="mt-8" v-if="seller">
              <h2 class="text-xl font-semibold">Продавец</h2>
              <div @click="navigateToSeller" class="flex cursor-pointer items-center space-x-4 border rounded-xl p-2 m-2">
                <Avatar 
                  image="/user.png" 
                  size="xlarge" 
                  shape="circle" 
                />
                <div>
                  <p class="text-xl text-gray-500">{{ seller.email }}</p>
                  <!-- <p class="text-xs text-gray-500" v-if="seller.inn">INN: {{ seller.inn }}</p> -->
                  <div class="flex items-center space-x-1">
                    <i class="pi pi-star text-yellow-400"></i>
                    <span class="text-sm">5 / 5</span>
                  </div>
                  <p class="text-xs text-gray-500" v-if="seller.seller_bio">{{ seller.seller_bio }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const isLoading = ref(true)
  const error = ref(null)
  
  const product = ref({
    photos: [],
    title: '',
    price: 0,
    description: '',
    category: '',
    type: '',
    seller_id: null
  })

  import { useCartStore } from '@/stores/cart';
  
  const cart = useCartStore();

  import { useToast } from 'primevue/usetoast';
  const toast = useToast();


  const addToCart = () => {
    const product2card = {
        id: route.params.id,
        name: product.value.title,
        price:  product.value.price,
        category: product.value.category,
        image: product.value.photos[0].photo
    };
    
    cart.addItem(product2card);
    toast.add({
          severity: 'success',
          summary: 'Успешно!',
          detail: 'Товар добавлен в корзину',
          life: 5000
        });
  };

  const navigateToSeller = (id) => {
    navigateTo(`/profile/${seller.value.id}`);
    };
  
  const seller = ref(null)
  const breadcrumbs = ref([])
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB'
    }).format(price)
  }
  
  const fetchProduct = async () => {
    try {
      const { type, category, id } = route.params
      
      // Initialize breadcrumbs with URL parameters
      breadcrumbs.value = [
        { label: 'Home', to: '/' },
        { 
          label: type, 
          to: `/products/${type}`
        },
        { 
          label: decodeURIComponent(category),
          to: `/products/${encodeURIComponent(type)}/${encodeURIComponent(category)}`
        },
        { label: 'Loading...', to: '' }
      ]
  
      const productResponse = await fetch(
        `http://127.0.0.1:8000/api/products/products/?id=${id}`
      )
      const productData = await productResponse.json()
      
      if (productData.length > 0 && productData[0].products.length > 0) {
        const apiProduct = productData[0].products[0]
        
        // Update product data
        product.value = {
          ...apiProduct,
          photos: apiProduct.photos.map(photo => ({ photo: photo.photo }))
        }
  
        // Update breadcrumbs with product title
        breadcrumbs.value[3] = {
          label: apiProduct.title,
          to: route.fullPath
        }
  
        // Fetch seller data
        if (apiProduct.seller_id) {
        //   const sellerResponse = await fetch(
        //     `http://127.0.0.1:8000/api/sellers/${apiProduct.seller_id}/`
        //   )
          const sellerData = {
            id: productData[0].products[0].seller_id,
            email: productData[0].products[0].seller_email,
            seller_bio: productData[0].products[0].seller_bio
          }
          seller.value = sellerData
        }
      }
    } catch (err) {
      error.value = 'Failed to load product data'
      console.error('Error:', err)
    } finally {
      isLoading.value = false
    }
  }
  
  onMounted(fetchProduct)


const op = ref();
const members = ref([
    { name: 'Amy Elsner', image: 'amyelsner.png', email: 'amy@email.com', role: 'Owner' },
    { name: 'Bernardo Dominic', image: 'bernardodominic.png', email: 'bernardo@email.com', role: 'Editor' },
    { name: 'Ioni Bowcher', image: 'ionibowcher.png', email: 'ioni@email.com', role: 'Viewer' }
]);

const toggle = (event) => {
    op.value.toggle(event);
}

  </script>
  
  <style scoped>
  :deep(.p-galleria-thumbnail-container) {
    @apply flex justify-center gap-2 mt-4;
  }
  
  :deep(.p-galleria-thumbnail-item) {
    @apply overflow-hidden rounded cursor-pointer transition-opacity duration-200;
  }
  
  :deep(.p-galleria-thumbnail-item:hover) {
    @apply opacity-75;
  }
  </style>