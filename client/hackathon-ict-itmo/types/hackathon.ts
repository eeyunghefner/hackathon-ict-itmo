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
}

export interface HackathonEvent {
  id: string
  name: string
  time: string
}