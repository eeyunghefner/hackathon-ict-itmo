<template>
  <div>
    <Navbar />

    <h1>Мои хакатоны</h1>

    <HackathonTable :hackathons="hackathons" />
  </div>
</template>

<script setup lang="ts">
import Navbar from "~/components/Navbar.vue"
import HackathonTable from "~/components/HackathonTable.vue"
import { useHackathonStore } from "~/stores/hackathonStore"

const hackathonStore = useHackathonStore()

const hackathons = hackathonStore.getHackathons
</script>