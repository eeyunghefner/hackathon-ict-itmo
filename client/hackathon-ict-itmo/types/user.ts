export interface UserProfileResponse {
  id: string
  firstName: string
  lastName: string
  email: string
  role: string
  teamId: string
}

export interface UpdateUserProfileRequest {
  firstName: string
  lastName: string
  university: string
}