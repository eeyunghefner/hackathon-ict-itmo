import { defineStore } from "pinia"

interface User {
  id: string
  email: string
  role: string
}

export const useAuthStore = defineStore("auth", {

  state: () => ({
    token: useCookie<string | null>("token").value || null,
    user: null as User | null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {

    async login(email: string, password: string) {
      const { $api } = useNuxtApp()

      const res = await $api<{
        token: string
        user: User
      }>("/auth/login", {
        method: "POST",
        body: { email, password }
      })

      this.token = res.token
      this.user = res.user

      const tokenCookie = useCookie("token")
      tokenCookie.value = res.token
    },

    async register(data: {
      email: string
      password: string
      firstName: string
      lastName: string
      university: string,
      isuNumber: string
    }) {
      const { $api } = useNuxtApp()

      const res = await $api<{
        id: string
        email: string
        role: string
        token: string
      }>("/auth/register", {
        method: "POST",
        body: data
      })

      this.token = res.token

      this.user = {
        id: res.id,
        email: res.email,
        role: res.role
      }

      const tokenCookie = useCookie("token")
      tokenCookie.value = res.token
    },

    logout() {
      this.token = null
      this.user = null

      const tokenCookie = useCookie("token")
      tokenCookie.value = null
    }

  }

})