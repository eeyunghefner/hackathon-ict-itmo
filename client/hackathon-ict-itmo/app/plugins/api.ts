export default defineNuxtPlugin(() => {

  const token = useCookie("token")

  const api = $fetch.create({
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
    provide: {
      api
    }
  }
})