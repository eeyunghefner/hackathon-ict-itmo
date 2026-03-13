import { defineStore } from "pinia"
import type {
  Hackathon,
  HackathonEvent,
  TeamRegistration,
  TeamApplication
} from "../../types/hackathon"

interface HackathonState {
  hackathons: Hackathon[]
  schedules: Record<string, HackathonEvent[]>
  registrations: Record<string, TeamRegistration[]>
  applications: Record<string, TeamApplication[]>
}

export const useHackathonStore = defineStore("hackathons", {

  state: (): HackathonState => ({
    hackathons: [
      {
        id: "1",
        name: "AI Hackathon",
        theme: "Artificial Intelligence",
        format: "online",
        description: "Hackathon about AI technologies",
        participantLimit: 100,
        teamLimit: 20,
        regulations: "Build AI project in 48 hours",
        published: true,
        organizerId: "1"
      }
    ],

    schedules: {
      "1": [
        { id: "1", name: "Opening", time: "10:00" }
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
    }

  }),

  getters: {

    getHackathons: (state) => state.hackathons,

    getOrganizerHackathons: (state) => {
      return (organizerId: string) =>
        state.hackathons.filter(h => h.organizerId === organizerId)
    },

    getHackathonById: (state) => {
      return (id: string) =>
        state.hackathons.find(h => h.id === id)
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
    }

  },

  actions: {

    addHackathon(hackathon: Hackathon) {
      this.hackathons.push(hackathon)
    },

    updateHackathon(updated: Hackathon) {
      const index = this.hackathons.findIndex(h => h.id === updated.id)
      if (index !== -1) {
        this.hackathons[index] = updated
      }
    },

    togglePublication(id: string) {
      const hackathon = this.hackathons.find(h => h.id === id)
      if (hackathon) {
        hackathon.published = !hackathon.published
      }
    },

    addEvent(hackathonId: string, event: HackathonEvent) {

      if (!this.schedules[hackathonId]) {
        this.schedules[hackathonId] = []
      }

      this.schedules[hackathonId].push(event)
    },

    removeEvent(hackathonId: string, eventId: string) {

      this.schedules[hackathonId] = (this.schedules[hackathonId] ?? []).filter(e => e.id !== eventId)
    }

  }

})