<template>
  <table>
    <thead>
      <tr>
        <th>Событие</th>
        <th>Время</th>
      </tr>
    </thead>

    <tbody>
      <tr v-for="event in events" :key="event.id">
        <td>{{ event.name }}</td>
        <td>{{ event.time }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
import type { HackathonEvent } from "../../types/hackathon"

defineProps<{
  events: HackathonEvent[]
}>()
</script>