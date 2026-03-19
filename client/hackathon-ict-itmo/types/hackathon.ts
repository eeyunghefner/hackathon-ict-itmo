export type HackathonFormat = "online" | "offline" | "hybrid"

export interface Hackathon {
  id: string
  name: string
  theme: string
  format: HackathonFormat
  description: string
  participantLimit: number
  teamLimit: number
  regulations: string
  published: boolean
  organizerId: string
}

export interface HackathonEvent {
  id: string
  name: string
  time: string
}

export interface TeamParticipant {
  id: string
  name: string
}

export interface TeamRegistration {
  id: string
  teamName: string
  members: TeamParticipant[]
}

export interface TeamApplication {
  id: string
  teamName: string
  members: TeamParticipant[]
}