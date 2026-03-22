<template>
  <table>
    <thead>
      <tr>
        <th>Название</th>
        <th>Формат</th>
        <th>Дата начала</th>
        <th>Статус</th>
      </tr>
    </thead>

    <tbody>
      <tr
        v-for="hackathon in hackathons"
        :key="hackathon.id"
        @click="goToHackathon(hackathon.id)"
      >
        <td>{{ hackathon.title }}</td>
        <td>{{ hackathon.format }}</td>
        <td>{{ hackathon.startDate }}</td>
        <td>{{ hackathon.status }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import type { HackathonListItem } from "../../types/hackathon"

const props = defineProps<{
  hackathons: HackathonListItem[]
}>()

const router = useRouter()

function goToHackathon(id: string) {
  router.push(`/hackathon/${id}`)
}
</script>