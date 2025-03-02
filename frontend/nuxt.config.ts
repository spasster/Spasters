// https://nuxt.com/docs/api/configuration/nuxt-config
import Aura from '@primeuix/themes/aura';
import { definePreset } from '@primeuix/themes'
import process from 'node:process'

const sw = process.env.SW === 'true'

const CustomBluePreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '{blue.50}',
      100: '{blue.100}',
      200: '{blue.200}',
      300: '{blue.300}',
      400: '{blue.400}',
      500: '{blue.500}',
      600: '{blue.600}',
      700: '{blue.700}',
      800: '{blue.800}',
      900: '{blue.900}',
      950: '{blue.950}'
    }
  }
})

export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  ssr: false,
  app: {
    head: {
      link: [{ rel: 'icon', type: 'image/png', href: '/logo.png' }]
    },
    meta: [
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'theme-color', content: '#2563eb' },
      { name: 'apple-mobile-web-app-capable', content: 'yes' },
      { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }
    ],
    link: [
      { rel: 'apple-touch-icon', href: '/pwa-192-192.png' }
    ]
  },
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@primevue/nuxt-module',
    '@productdevbook/chatwoot',
    '@vite-pwa/nuxt'
  ],
  primevue: {
    options: {
        ripple: true,
        inputVariant: 'filled',
        theme: {
            preset: CustomBluePreset,
            options: {
                prefix: 'p',
                darkModeSelector: '.dark',
                cssLayer: false
            }
        }
    }
  },
  pwa: {
    strategies: sw ? 'injectManifest' : 'generateSW',
    srcDir: sw ? 'service-worker' : undefined,
    filename: sw ? 'sw.ts' : undefined,
    registerType: 'autoUpdate',
    manifest: {
      name: 'Spasters',
      short_name: 'Spasters',
      theme_color: '#000000',
      icons: [
        {
          src: 'pwa-192-192.png',
          sizes: '192x192',
          type: 'image/png',
        },
        {
          src: 'pwa-512-512.png',
          sizes: '512x512',
          type: 'image/png',
        },
        {
          src: 'pwa-512-512.png',
          sizes: '512x512',
          type: 'image/png',
          purpose: 'any maskable',
        },
      ],
    },
    workbox: {
      globPatterns: ['**/*.{js,css,html,png,svg,ico}'],
    },
    injectManifest: {
      globPatterns: ['**/*.{js,css,html,png,svg,ico}'],
    },
    client: {
      installPrompt: true,
      // you don't need to include this: only for testing purposes
      // if enabling periodic sync for update use 1 hour or so (periodicSyncForUpdates: 3600)
      periodicSyncForUpdates: 20,
    },
    devOptions: {
      enabled: true,
      suppressWarnings: true,
      navigateFallback: '/',
      navigateFallbackAllowlist: [/^\/$/],
      type: 'module',
    }
  },
  chatwoot: {
    init: {
      websiteToken: 'hgtcfHPGX3n9AGjoPXKbiqVz'
    },
    settings: {
      locale: 'ru',
      position: 'right',
      launcherTitle: 'Нужна помощь?',
      // ... and more settings
    },
    // If this is loaded you can make it true, https://github.com/nuxt-modules/partytown
    partytown: false,
  },
  css: [
    'primeicons/primeicons.css',
    'primeflex/primeflex.css',
    '~/assets/css/main.css',
    '~/assets/css/tailwind.css'
  ]
})