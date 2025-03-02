<template>
    <button
      @click="toggleTheme"
      class="relative flex items-center justify-between w-16 h-8 rounded-full p-1 transition-all duration-300 bg-transperent focus:outline-none ring-2 focus:ring-primary-500"
      aria-label="Toggle theme"
    >
      <!-- Icons Container -->
      <div class="flex items-center justify-between w-full px-1">
        <!-- Sun Icon (Light) -->
        <svg
          class="w-5 h-5 text-yellow-500 transition-all duration-300 dark:text-yellow-400"
          :class="{
            'opacity-100 translate-x-0': !isDark,
            'opacity-0 -translate-x-3': isDark,
          }"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z"
          />
        </svg>
  
        <!-- Moon Icon (Dark) -->
        <svg
          class="w-5 h-5 text-blue-500 transition-all duration-300 dark:text-blue-400"
          :class="{
            'opacity-100 translate-x-0': isDark,
            'opacity-0 translate-x-3': !isDark,
          }"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z"
          />
        </svg>
      </div>
  
      <!-- Toggle Ball -->
      <div
        class="absolute top-1 left-[5px] bg-gray-700 opacity-30 w-5 h-6 rounded-full shadow-lg transform transition-all duration-300"
        :class="{
          'translate-x-7': isDark,
          'translate-x-0': !isDark,
        }"
      ></div>
    </button>
  </template>
  
  <script setup>
  const isDark = ref(false)
  
  // Theme initialization
  onMounted(() => {
    const savedTheme = localStorage.getItem('theme')
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    
    isDark.value = savedTheme 
      ? savedTheme === 'dark'
      : systemDark
  
    updateThemeClass()
  })
  
  // Toggle theme function
  const toggleTheme = () => {
    isDark.value = !isDark.value
    updateThemeClass()
    localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  }
  
  // Update DOM class
  const updateThemeClass = () => {
    document.documentElement.classList.toggle('dark', isDark.value)
  }
  </script>