import { defineStore } from "pinia"
import type { UpdateUserProfileRequest, UserProfileResponse } from "../../types/user"

export const useUserStore = defineStore("user", {

  state: () => ({
    user: null as UserProfileResponse | null,
    university: "",
    loading: false
  }),

  getters: {
    getUser: (state) => state.user
  },

  actions: {
    async fetchMyProfile() {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<UserProfileResponse>("/users/me", {
        baseURL: config.public.apiBase,
        headers: token.value
          ? { Authorization: `Bearer ${token.value}` }
          : undefined
      })

      this.loading = false

      if (error.value) {
        throw error.value
      }

      if (!data.value) {
        throw new Error("Profile response is empty")
      }

      this.user = data.value
      return data.value
    },

    async updateMyProfile(payload: UpdateUserProfileRequest) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch("/users/me", {
        baseURL: config.public.apiBase,
        method: "PATCH",
        body: payload,
        headers: token.value
          ? { Authorization: `Bearer ${token.value}` }
          : undefined
      })

      this.loading = false

      if (error.value) {
        throw error.value
      }

      return await this.fetchMyProfile()
    }
  }

})