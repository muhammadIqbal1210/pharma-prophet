// nuxt.config.ts
export default defineNuxtConfig({
  ssr: false,

  app: {
    head: {
      title: 'PharmaCast - Sistem Prediksi & Manajemen Stok Apotek',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },
  css: [
    '~/assets/css/main.css'
  ],
  
  runtimeConfig: {
    public: {
      // Ganti process.env menjadi import.meta.env
      apiBase: import.meta.env.API_BASE_URL || 'http://localhost:8000/api/v1'
    }
  },

  compatibilityDate: '2026-05-18'
})