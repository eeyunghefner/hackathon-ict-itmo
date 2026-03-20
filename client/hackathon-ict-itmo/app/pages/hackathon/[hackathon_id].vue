<template>
  <Card>
    <h1>{{ hackathon?.title }}</h1>
    <p>{{ hackathon?.description }}</p>
  </Card>

  <Card>
    <h2>Расписание</h2>
    <Table
      :headers="['Событие', 'Время']"
      :rows="eventsRows"
    />
  </Card>
</template>

<script setup lang="ts">
import { computed } from "vue"
import { useRoute } from 'vue-router'
import { useHackathonStore } from '~/stores/hackathonStore'
import Card from '~/components/ui/Card.vue'
import Table from '~/components/ui/Table.vue'
import type { HackathonEvent } from "../../../types/hackathon"

const route = useRoute()
const store = useHackathonStore()
const id = route.params.hackathon_id as string

onMounted(() => {
  // Store keeps cache, but ensure we request details from API
  store.fetchHackathon(id).catch((e) => console.error(e))
  store.fetchEvents(id).catch((e) => console.error(e))
})

const hackathon = computed(() => store.getHackathonById(id))
const events = computed(() => store.getSchedule(id))

function formatEventTime(e: HackathonEvent) {
  const start = e.startTime ?? e.time
  const end = e.endTime
  if (start && end) return `${start} - ${end}`
  return start ?? ''
}

const eventsRows = computed(() => {
  return events.value.map((e: HackathonEvent) => [
    e.title ?? e.name ?? "—",
    formatEventTime(e)
  ])
})
</script>