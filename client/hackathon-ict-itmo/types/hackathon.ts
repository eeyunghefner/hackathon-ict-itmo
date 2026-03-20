export type HackathonFormat = "online" | "offline" | "hybrid"
export type HackathonStatus = "draft" | "published" | "archived"

// 3.1 Создать хакатон
export interface CreateHackathonRequest {
  title: string
  theme: string
  format: HackathonFormat
  description: string
  startDate: string // YYYY-MM-DD
  endDate: string // YYYY-MM-DD
  participantLimit: number
  teamLimit: number
  rules: string
}

export interface CreateHackathonResponse {
  id: string
  status: "draft"
}

// 3.2 Получить список хакатонов
export interface GetHackathonsQuery {
  status?: HackathonStatus
  page?: number
  limit?: number
}

export interface HackathonListItem {
  id: string
  title: string
  format: HackathonFormat
  startDate: string // YYYY-MM-DD
  status: HackathonStatus
}

// 3.3 Получить один хакатон
export interface HackathonDetail {
  id: string
  title: string
  theme: string
  description: string
  format: HackathonFormat
  startDate: string // YYYY-MM-DD
  endDate: string // YYYY-MM-DD
  participantLimit: number
  teamLimit: number
  rules: string
  status: HackathonStatus
}

// 3.4 Редактировать хакатон
export type UpdateHackathonRequest = Partial<Pick<
  CreateHackathonRequest,
  "title" | "theme" | "format" | "description" | "startDate" | "endDate" | "participantLimit" | "teamLimit" | "rules"
>>

export interface HackathonEvent {
  id: string
  // New API shape
  title?: string
  description?: string
  startTime?: string
  endTime?: string
  roomId?: string

  // Legacy fields (currently used in some UI screens)
  name?: string
  time?: string
}

export interface CreateHackathonEventRequest {
  title: string
  description?: string
  startTime: string
  endTime: string
  roomId: string
}

export type UpdateHackathonEventRequest = Partial<CreateHackathonEventRequest>

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

// 4.* Заявки команды на хакатон
export type HackathonApplicationStatus = "pending" | "approved" | "rejected"

export interface HackathonApplication {
  id: string
  teamId: string
  teamName: string
  status: HackathonApplicationStatus
}

export interface CreateHackathonApplicationRequest {
  teamId: string
}