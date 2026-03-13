<template>
  <div>
    <h1>Поиск команд</h1>

    <input v-model="search" placeholder="Поиск команды" />

    <TeamTable :teams="filteredTeams" />
  </div>
</template>

<script setup lang="ts">
import Navbar from "~/components/Navbar.vue"
import TeamTable from "~/components/TeamTable.vue"
import { useTeamStore } from "~/stores/teamStore"
import { ref, computed } from "vue"

const teamStore = useTeamStore()

const search = ref("")

const filteredTeams = computed(() =>
  teamStore.searchTeams(search.value)
)
</script>