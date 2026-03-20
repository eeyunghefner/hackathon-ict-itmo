<template>
  <Card>
    <div class="header-row">
      <h1>Команды</h1>
      <NuxtLink :to="{ path: '/team/add', query: hackathonId ? { hackathonId } : {} }">
        <Button variant="primary">Создать команду</Button>
      </NuxtLink>
    </div>
    <FormField label="Поиск" v-model="query" type="input" />
  </Card>

  <TeamTable :teams="filteredTeams" />
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useTeamStore } from '~/stores/teamStore'
import Card from '~/components/ui/Card.vue'
import FormField from '~/components/ui/FormField.vue'
import Button from '~/components/ui/Button.vue'
import TeamTable from '~/components/TeamTable.vue'
import { type TeamListItem } from '../../types/team'

const query = ref('')
const route = useRoute()
const store = useTeamStore()

const hackathonId = computed(() => {
  const v = route.query.hackathonId
  return typeof v === "string" && v.length ? v : undefined
})

const filteredTeams = computed(() => {
  return store.searchTeams(query.value) as TeamListItem[]
})

onMounted(() => {
  store.fetchTeams(hackathonId.value).catch((e) => console.error(e))
})

watch(hackathonId, (id) => {
  store.fetchTeams(id).catch((e) => console.error(e))
})
</script>

<style scoped>
.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>