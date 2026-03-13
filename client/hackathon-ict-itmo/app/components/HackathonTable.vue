<template>
  <table>
    <thead>
      <tr>
        <th>Название</th>
        <th>Тематика</th>
        <th>Формат</th>
        <th>Описание</th>
        <th>Лимит участников</th>
        <th>Лимит команд</th>
        <th>Регламент</th>
      </tr>
    </thead>

    <tbody>
      <tr
        v-for="hackathon in hackathons"
        :key="hackathon.id"
        @click="goToHackathon(hackathon.id)"
      >
        <td>{{ hackathon.name }}</td>
        <td>{{ hackathon.theme }}</td>
        <td>{{ hackathon.format }}</td>
        <td>{{ hackathon.description }}</td>
        <td>{{ hackathon.participantLimit }}</td>
        <td>{{ hackathon.teamLimit }}</td>
        <td>{{ hackathon.regulations }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import type { Hackathon } from "../../types/hackathon"

const props = defineProps<{
  hackathons: Hackathon[]
}>()

const router = useRouter()

function goToHackathon(id: string) {
  router.push(`/hackathon/${id}`)
}
</script>