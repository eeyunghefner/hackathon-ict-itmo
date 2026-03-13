<template>
  <div>
    <Navbar />

    <h1>{{ hackathon?.name }}</h1>

    <ScheduleTable :events="events" />
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router"
import Navbar from "~/components/Navbar.vue"
import ScheduleTable from "~/components/ScheduleTable.vue"
import { useHackathonStore } from "~/stores/hackathonStore"

const route = useRoute()

const hackathonStore = useHackathonStore()

const id = route.params.hackathon_id as string

const hackathon = hackathonStore.getHackathonById(id)

const events = hackathonStore.getSchedule(id)
</script>