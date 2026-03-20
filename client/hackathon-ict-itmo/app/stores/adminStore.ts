import { defineStore } from "pinia"
import type { AdminUser, UserRole } from "../../types/user"

interface AdminState {
  users: AdminUser[]
  loading: boolean
}

const roles: UserRole[] = ["participant", "organizer", "admin"]

export const useAdminStore = defineStore("admin", {
  state: (): AdminState => ({
    users: [],
    loading: false
  }),

  getters: {
    getUsers: (state) => state.users
  },

  actions: {
    async fetchUsersByRole(role: UserRole, page = 1) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      const { data, error } = await useFetch<AdminUser[]>("/admin/users", {
        baseURL: config.public.apiBase,
        method: "GET",
        query: { role, page },
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      if (error.value) throw error.value
      return data.value ?? []
    },

    async fetchAllUsers(page = 1) {
      this.loading = true

      try {
        const results = await Promise.all(
          roles.map(async (role) => {
            try {
              return await this.fetchUsersByRole(role, page)
            } catch {
              return []
            }
          })
        )

        const byId = new Map<string, AdminUser & { _rolesSet?: Set<UserRole> }>()
        roles.forEach((role, roleIdx) => {
          for (const u of results[roleIdx]) {
            const existing = byId.get(u.id)
            if (!existing) {
              byId.set(u.id, { ...u, roles: [], _rolesSet: new Set<UserRole>() })
            }

            const entry = byId.get(u.id)!
            entry._rolesSet!.add(role)
          }
        })

        const merged = Array.from(byId.values()).map((u) => ({
          id: u.id,
          firstName: u.firstName,
          lastName: u.lastName,
          email: u.email,
          roles: Array.from(u._rolesSet ?? new Set<UserRole>())
        }))

        this.users = merged
        return merged
      } finally {
        this.loading = false
      }
    },

    async assignRole(userId: string, role: UserRole) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      const { error } = await useFetch(`/admin/users/${userId}`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        body: { role },
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      if (error.value) throw error.value
    },

    async deleteUser(userId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      const { error } = await useFetch(`/admin/users/${userId}`, {
        baseURL: config.public.apiBase,
        method: "DELETE",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      if (error.value) throw error.value
    }
  }
})

