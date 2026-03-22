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
    // let data = [] as HackathonListItem[]
        //       try {
        //         data = await $fetch<HackathonListItem[]>("/hackathons", {
        //         baseURL: config.public.apiBase,
        //         method: "GET",
        //         query,
        //         headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
        //       })
        //      } catch (e) {
        //         throw e
        //       }
    async fetchMyProfile() {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      let data = null as UserProfileResponse | null
      try {
        data = await $fetch<UserProfileResponse>("/users/me", {
        baseURL: config.public.apiBase,
        method: "GET",
        headers: token.value
          ? { Authorization: `Bearer ${token.value}` }
          : undefined
      })
      } catch (e) {
        return e
      }
      
      this.loading = false


      if (!data) {
        throw new Error("Profile response is empty")
      }

      this.user = data
      return data
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