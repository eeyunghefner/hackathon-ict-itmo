// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',

  runtimeConfig: {
    public: {
      apiBase: "http://localhost:3000"
    }
  },
  
  devtools: { enabled: true },

  modules: ['@pinia/nuxt'],

  srcDir: "app",

  css: [
    "@/assets/css/main.css"
  ],
  app: {
    head: {
      link: [
        {
          rel: "stylesheet",
          href: "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap"
        }
      ]
    }
  }
})