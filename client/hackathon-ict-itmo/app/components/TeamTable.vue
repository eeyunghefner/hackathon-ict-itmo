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
        <td>{{ team.name }}</td>
        <td>{{ getTeamMembersCount(team) }}</td>
        <td>
          <button @click="apply(team.id)">Подать заявку</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router"
import { getTeamMembersCount, type TeamListItem } from "../../types/team"

const router = useRouter()

defineProps<{
  teams: TeamListItem[]
}>()

function apply(id: string) {
  router.push({ path: "/hackathons/apply", query: { teamId: id } })
}
</script>