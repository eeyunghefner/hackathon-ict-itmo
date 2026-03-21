import { defineStore } from "pinia"
import type { CreateTeamRequest, TeamDetail, TeamJoinRequest, TeamListItem } from "../../types/team"

interface TeamState {
  teams: TeamListItem[]
  teamById: Record<string, TeamDetail | undefined>
  joinRequestsByTeamId: Record<string, TeamJoinRequest[]>
  loading: boolean
}

export const useTeamStore = defineStore("teams", {

  state: (): TeamState => ({
    teams: [],
    teamById: {},
    joinRequestsByTeamId: {},
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
    ,

    getJoinRequests: (state) => {
      return (teamId: string) => state.joinRequestsByTeamId[teamId] || []
    }

  },

  actions: {
    async fetchTeams(hackathonId?: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const query = hackathonId ? { hackathonId } : undefined

      let data = [] as TeamListItem[]
      try {
        data = await $fetch<TeamListItem[]>("/teams", {
        baseURL: config.public.apiBase,
        method: "GET",
        query,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })
      } catch (e) {
        return e
      }
      
      this.loading = false

      if (!data) throw new Error("Teams response is empty")

      this.teams = data
      return data
    },

    async fetchTeam(teamId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true
      let data = null as TeamDetail | null
      try {
        data = await $fetch<TeamDetail>(`/teams/${teamId}`, {
        baseURL: config.public.apiBase,
        method: "GET",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })
      } catch (e) {
        throw e
      }
      

      this.loading = false

      if (!data) throw new Error("Team response is empty")

      this.teamById[teamId] = data
      return data
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
    },

    // 5.4 Исключить участника команды
    async excludeMember(teamId: string, userId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/teams/${teamId}/members/${userId}`, {
        baseURL: config.public.apiBase,
        method: "DELETE",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value

      // Перезагружаем команду, чтобы обновить список участников и captainId.
      await this.fetchTeam(teamId)
    },

    // 5.5 Назначить капитана
    async setCaptain(teamId: string, userId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/teams/${teamId}/captain`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        body: { userId },
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value

      await this.fetchTeam(teamId)
    },

    // 6.1 Подать заявку в команду
    async submitJoinRequest(teamId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/teams/${teamId}/join-request`, {
        baseURL: config.public.apiBase,
        method: "POST",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value

      // Обновим список заявок на случай, если UI сразу переключится.
      // await this.fetchJoinRequests(teamId)
    },

    // 6.2 Получить заявки команды (кастом-данные под UI)
    async fetchJoinRequests(teamId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      let data = [] as TeamJoinRequest[]
      try {
        data = await $fetch<TeamJoinRequest[]>(
        `/teams/${teamId}/join-requests`,
        {
          baseURL: config.public.apiBase,
          method: "GET",
          headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
        }
      )
      } catch (e) {
        throw e
      }
      

      this.loading = false

      if (!data) throw new Error("Join requests response is empty")

      this.joinRequestsByTeamId[teamId] = data
      return data
    },

    // 6.3 Принять заявку
    async approveJoinRequest(requestId: string, teamId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/team-requests/${requestId}/approve`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value

      return await this.fetchJoinRequests(teamId)
    },

    // 6.4 Отклонить заявку
    async rejectJoinRequest(requestId: string, teamId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/team-requests/${requestId}/reject`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value

      return await this.fetchJoinRequests(teamId)
    }

  }

})