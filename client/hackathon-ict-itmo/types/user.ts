export interface UserProfileResponse {
  id: string
  firstName: string
  lastName: string
  email: string
  roles: string []
  teamId: string
  university: string
}

export interface UpdateUserProfileRequest {
  firstName: string
  lastName: string
  university: string
}