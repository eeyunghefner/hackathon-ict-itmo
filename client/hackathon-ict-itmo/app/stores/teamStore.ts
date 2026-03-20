import { defineStore } from "pinia"
import type { CreateTeamRequest, TeamDetail, TeamListItem } from "../../types/team"

interface TeamState {
  teams: TeamListItem[]
  teamById: Record<string, TeamDetail | undefined>
  loading: boolean
}

export const useTeamStore = defineStore("teams", {

  state: (): TeamState => ({
    teams: [],
    teamById: {},
    loading: false
  }),

  getters: {

    getTeams: (state) => state.teams,

    searchTeams: (state) => {
      return (query: string) => {

        if (!query) return state.teams

        return state.teams.filter((team) =>
          team.name.toLowerCase().includes(query.toLowerCase())
        )
      }
    },

    getTeamById: (state) => {
      return (id: string) => state.teamById[id]
    }

  },

  actions: {
    async fetchTeams(hackathonId?: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const query = hackathonId ? { hackathonId } : undefined

      const { data, error } = await useFetch<TeamListItem[]>("/teams", {
        baseURL: config.public.apiBase,
        method: "GET",
        query,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      if (!data.value) throw new Error("Teams response is empty")

      this.teams = data.value
      return data.value
    },

    async fetchTeam(teamId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<TeamDetail>(`/teams/${teamId}`, {
        baseURL: config.public.apiBase,
        method: "GET",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      if (!data.value) throw new Error("Team response is empty")

      this.teamById[teamId] = data.value
      return data.value
    },

    async createTeam(payload: CreateTeamRequest) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<{ id: string }>(`/teams`, {
        baseURL: config.public.apiBase,
        method: "POST",
        body: payload,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      if (!data.value) throw new Error("Create team response is empty")

      return data.value
    },

    async leaveTeam(teamId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/teams/${teamId}/leave`, {
        baseURL: config.public.apiBase,
        method: "POST",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value

      // Оптимистично убираем из локального кэша.
      this.teams = this.teams.filter((t) => t.id !== teamId)
      delete this.teamById[teamId]
    }

  }

})