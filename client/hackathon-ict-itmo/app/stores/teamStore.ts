import { defineStore } from "pinia"
import type { Team } from "../../types/team"

interface TeamState {
  teams: Team[]
}

export const useTeamStore = defineStore("teams", {

  state: (): TeamState => ({
    teams: [
      { id: "1", name: "Code Masters", members: 4 },
      { id: "2", name: "AI Warriors", members: 3 },
      { id: "3", name: "Hack Squad", members: 5 }
    ]
  }),

  getters: {

    getTeams: (state) => state.teams,

    searchTeams: (state) => {
      return (query: string) => {

        if (!query) return state.teams

        return state.teams.filter(team =>
          team.name.toLowerCase().includes(query.toLowerCase())
        )
      }
    }

  },

  actions: {

    addTeam(team: Team) {
      this.teams.push(team)
    },

    applyToTeam(teamId: string) {
      console.log("Apply to team", teamId)
    }

  }

})