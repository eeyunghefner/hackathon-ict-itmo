<template>
  <Card>
    <h1>{{ hackathon?.title }}</h1>
    <p>{{ hackathon?.description }}</p>
  </Card>

  <Card>
    <h2>Расписание</h2>
    <Table
      :headers="['Событие', 'Время']"
      :rows="events.map(e => [e.name, e.time])"
    />
  </Card>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useHackathonStore } from '~/stores/hackathonStore'
import Card from '~/components/ui/Card.vue'
import Table from '~/components/ui/Table.vue'

const route = useRoute()
const store = useHackathonStore()
const id = route.params.hackathon_id as string

onMounted(() => {
  // Store keeps cache, but ensure we request details from API
  store.fetchHackathon(id).catch((e) => console.error(e))
})

const hackathon = computed(() => store.getHackathonById(id))
const events = store.getSchedule(id)
</script>