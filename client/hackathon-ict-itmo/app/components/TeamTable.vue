<template>
  <table>
    <thead>
      <tr>
        <th>Название</th>
        <th>Количество участников</th>
        <th></th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="team in teams" :key="team.id">
        <td>
          <NuxtLink :to="`/team/${team.id}`">{{ team.name }}</NuxtLink>
        </td>
        <td>{{ getTeamMembersCount(team) }}</td>
        <td>
          <button @click="submit(team.id)" :disabled="submittingId === team.id">
            {{ submittingId === team.id ? "Отправка..." : "Подать заявку в команду" }}
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { getTeamMembersCount, type TeamListItem } from "../../types/team"
import { useTeamStore } from "~/stores/teamStore"

defineProps<{
  teams: TeamListItem[]
}>()

const store = useTeamStore()
const submittingId = ref<string | null>(null)

async function submit(teamId: string) {
  try {
    submittingId.value = teamId
    await store.submitJoinRequest(teamId)
    alert("Заявка отправлена")
  } catch (e) {
    console.error(e)
    alert("Не удалось отправить заявку")
  } finally {
    submittingId.value = null
  }
}
</script>