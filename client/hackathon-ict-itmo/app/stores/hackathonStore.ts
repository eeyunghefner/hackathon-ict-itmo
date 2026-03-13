import { defineStore } from "pinia"
import type { Hackathon, HackathonEvent } from "../../types/hackathon"

interface HackathonState {
  hackathons: Hackathon[]
  schedules: Record<string, HackathonEvent[]>
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
        regulations: "Build AI project in 48 hours"
      },
      {
        id: "2",
        name: "FinTech Hackathon",
        theme: "Finance Technologies",
        format: "offline",
        description: "Solve financial problems",
        participantLimit: 80,
        teamLimit: 15,
        regulations: "Create fintech prototype"
      }
    ],

    schedules: {
      "1": [
        { id: "1", name: "Opening Ceremony", time: "10:00" },
        { id: "2", name: "Team Formation", time: "11:00" },
        { id: "3", name: "Project Development", time: "12:00" }
      ],

      "2": [
        { id: "1", name: "Welcome Speech", time: "09:00" },
        { id: "2", name: "Hacking Begins", time: "10:00" }
      ]
    }
  }),

  getters: {

    getHackathons: (state) => state.hackathons,

    getHackathonById: (state) => {
      return (id: string) =>
        state.hackathons.find(h => h.id === id)
    },

    getScheduleByHackathonId: (state) => {
      return (id: string) =>
        state.schedules[id] || []
    }

  },

  actions: {

    addHackathon(hackathon: Hackathon) {
      this.hackathons.push(hackathon)
    },

    addEvent(hackathonId: string, event: HackathonEvent) {

      if (!this.schedules[hackathonId]) {
        this.schedules[hackathonId] = []
      }

      this.schedules[hackathonId].push(event)
    }

  }

})