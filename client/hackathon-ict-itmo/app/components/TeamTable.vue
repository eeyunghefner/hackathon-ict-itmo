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
        <td>{{ team.members }}</td>
        <td>
          <button @click="apply(team.id)">Подать заявку</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import type { Team } from "../../types/team"

defineProps<{
  teams: Team[]
}>()

function apply(id: string) {
  console.log("Apply to team", id)
}
</script>