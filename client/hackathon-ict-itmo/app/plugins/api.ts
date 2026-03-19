export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const api = $fetch.create({
    baseURL: config.public.apiBase,
    onRequest({ options }) {
      const token = useCookie("token")

      if (token.value) {
        if (!options.headers) {
          options.headers = new Headers()
        }

        if (options.headers instanceof Headers) {
          options.headers.set("Authorization", `Bearer ${token.value}`)
        }
      }
    }
  })

  return {
    provide: { api }
  }
})