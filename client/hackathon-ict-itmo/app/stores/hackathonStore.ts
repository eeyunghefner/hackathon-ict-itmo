import { defineStore } from "pinia"
import type {
  CreateHackathonRequest,
  CreateHackathonResponse,
  CreateHackathonApplicationRequest,
  CreateHackathonEventRequest,
  GetHackathonsQuery,
  HackathonDetail,
  HackathonApplication,
  HackathonEvent,
  HackathonListItem,
  TeamRegistration,
  TeamApplication,
  UpdateHackathonEventRequest,
  UpdateHackathonRequest
} from "../../types/hackathon"

interface HackathonState {
  hackathons: HackathonListItem[]
  hackathonById: Record<string, HackathonDetail | undefined>
  schedules: Record<string, HackathonEvent[]>
  registrations: Record<string, TeamRegistration[]>
  applications: Record<string, TeamApplication[]>
  hackathonApplications: Record<string, HackathonApplication[]>
  loading: boolean
}

export const useHackathonStore = defineStore("hackathons", {

  state: (): HackathonState => ({
    hackathons: [],
    hackathonById: {},

    schedules: {
      "1": [
        {
          id: "1",
          // Legacy fields used by some UI
          name: "Opening Ceremony",
          time: "10:00",
          // New API shape
          title: "Opening Ceremony",
          description: "Opening speech",
          startTime: "2026-05-10T10:00",
          endTime: "2026-05-10T11:00",
          roomId: "00000000-0000-0000-0000-000000000000"
        }
      ]
    },

    registrations: {
      "1": [
        {
          id: "1",
          teamName: "Code Masters",
          members: [
            { id: "1", name: "Ivan" },
            { id: "2", name: "Anna" }
          ]
        }
      ]
    },

    applications: {
      "1": [
        {
          id: "1",
          teamName: "Hack Squad",
          members: [
            { id: "1", name: "Alex" }
          ]
        }
      ]
    },
    hackathonApplications: {},

    loading: false
  }),

  getters: {

    getHackathons: (state) => state.hackathons,

    getHackathonById: (state) => {
      return (id: string) =>
        state.hackathonById[id]
    },

    getSchedule: (state) => {
      return (id: string) =>
        state.schedules[id] || []
    },

    getRegistrations: (state) => {
      return (id: string) =>
        state.registrations[id] || []
    },

    getApplications: (state) => {
      return (id: string) =>
        state.applications[id] || []
    },

    // 4.2 Получить заявки хакатона (организатор)
    getHackathonApplications: (state) => {
      return (hackathonId: string) =>
        state.hackathonApplications[hackathonId] || []
    }

  },

  actions: {

    async createHackathon(payload: CreateHackathonRequest) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<CreateHackathonResponse>("/hackathons", {
        baseURL: config.public.apiBase,
        method: "POST",
        body: payload,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      if (!data.value) throw new Error("Create hackathon response is empty")

      return data.value
    },

    async fetchHackathons(query: GetHackathonsQuery = {}) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<HackathonListItem[]>("/hackathons", {
        baseURL: config.public.apiBase,
        query,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      if (!data.value) throw new Error("Hackathons list response is empty")

      this.hackathons = data.value
      return data.value
    },

    async fetchHackathon(hackathonId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<HackathonDetail>(`/hackathons/${hackathonId}`, {
        baseURL: config.public.apiBase,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      if (!data.value) throw new Error("Hackathon response is empty")

      this.hackathonById[hackathonId] = data.value
      return data.value
    },

    async updateHackathon(hackathonId: string, payload: UpdateHackathonRequest) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/hackathons/${hackathonId}`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        body: payload,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      return await this.fetchHackathon(hackathonId)
    },

    async publishHackathon(hackathonId: string) {
      return await this._transitionStatus(hackathonId, "publish")
    },

    async unpublishHackathon(hackathonId: string) {
      return await this._transitionStatus(hackathonId, "unpublish")
    },

    async archiveHackathon(hackathonId: string) {
      return await this._transitionStatus(hackathonId, "archive")
    },

    async _transitionStatus(hackathonId: string, action: "publish" | "unpublish" | "archive") {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/hackathons/${hackathonId}/${action}`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      return await this.fetchHackathon(hackathonId)
    },

    // 4.1 Подать заявку команды
    async submitHackathonApplication(hackathonId: string, payload: CreateHackathonApplicationRequest) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/hackathons/${hackathonId}/applications`, {
        baseURL: config.public.apiBase,
        method: "POST",
        body: payload,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value

      // if organizer is viewing, refresh list
      await this.fetchHackathonApplications(hackathonId)
    },

    // 4.2 Получить заявки хакатона (организатор)
    async fetchHackathonApplications(hackathonId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<HackathonApplication[]>(
        `/hackathons/${hackathonId}/applications`,
        {
          baseURL: config.public.apiBase,
          method: "GET",
          headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
        }
      )

      this.loading = false

      if (error.value) throw error.value
      if (!data.value) throw new Error("Hackathon applications response is empty")

      this.hackathonApplications[hackathonId] = data.value
      return data.value
    },

    // 4.3 Одобрить заявку
    async approveHackathonApplication(applicationId: string, hackathonId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/applications/${applicationId}/approve`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      return await this.fetchHackathonApplications(hackathonId)
    },

    // 4.4 Отклонить заявку
    async rejectHackathonApplication(applicationId: string, hackathonId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/applications/${applicationId}/reject`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      return await this.fetchHackathonApplications(hackathonId)
    },

    // 9.2 Получить расписание
    async fetchEvents(hackathonId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { data, error } = await useFetch<HackathonEvent[]>(
        `/hackathons/${hackathonId}/events`,
        {
          baseURL: config.public.apiBase,
          method: "GET",
          headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
        }
      )

      this.loading = false

      if (error.value) throw error.value
      this.schedules[hackathonId] = data.value ?? []
      return this.schedules[hackathonId]
    },

    // 9.1 Добавить событие
    async createEvent(hackathonId: string, payload: CreateHackathonEventRequest) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/hackathons/${hackathonId}/events`, {
        baseURL: config.public.apiBase,
        method: "POST",
        body: payload,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      return await this.fetchEvents(hackathonId)
    },

    // 9.3 Редактировать событие
    async updateEvent(
      eventId: string,
      hackathonId: string,
      payload: UpdateHackathonEventRequest
    ) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/events/${eventId}`, {
        baseURL: config.public.apiBase,
        method: "PATCH",
        body: payload,
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      return await this.fetchEvents(hackathonId)
    },

    // 9.4 Удалить событие
    async deleteEvent(eventId: string, hackathonId: string) {
      const config = useRuntimeConfig()
      const token = useCookie<string | null>("token")

      this.loading = true

      const { error } = await useFetch(`/events/${eventId}`, {
        baseURL: config.public.apiBase,
        method: "DELETE",
        headers: token.value ? { Authorization: `Bearer ${token.value}` } : undefined
      })

      this.loading = false

      if (error.value) throw error.value
      return await this.fetchEvents(hackathonId)
    }

  }

})