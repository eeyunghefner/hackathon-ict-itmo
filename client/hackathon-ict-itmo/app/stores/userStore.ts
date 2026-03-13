import { defineStore } from "pinia"
import type { User } from "../../types/user"

export const useUserStore = defineStore("user", {

  state: (): { user: User } => ({
    user: {
      fullName: "Ivan Ivanov",
      education: "Computer Science",
      skills: "Vue, TypeScript, Python",
      description: "Passionate developer"
    }
  }),

  getters: {
    getUser: (state) => state.user
  },

  actions: {
    updateUser(newUser: User) {
      this.user = newUser
    },

    updateField<K extends keyof User>(field: K, value: User[K]) {
      this.user[field] = value
    }
  }

})