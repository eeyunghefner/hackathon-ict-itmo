export interface TeamMember {
  id: string
  name: string
}

// 5.3 Получить команду
export interface TeamDetail {
  id: string
  name: string
  captainId: string
  members: TeamMember[]
}

// 5.1 Создать команду
export interface CreateTeamRequest {
  name: string
  description: string
}

// 5.2 Получить команды (response в условии не указан).
// Поэтому members/captainId/fallback-поля делаем опциональными, чтобы UI мог отрисовать количество участников.
export interface TeamListItem {
  id: string
  name: string
  captainId?: string
  members?: TeamMember[]
  membersCount?: number
}

export function getTeamMembersCount(team: TeamListItem | TeamDetail): number {
  if (typeof (team as TeamDetail).members !== "undefined") return (team as TeamDetail).members.length
  if (typeof team.membersCount === "number") return team.membersCount
  return 0
}