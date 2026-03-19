<template>
  <div>
    <Card>
      <h1>Мои хакатоны</h1>
    </Card>

    <Table
      :headers="['Название', 'Тематика', 'Формат']"
      :rows="hackathons.map(h => [h.name, h.theme, h.format])"
      @row-click="goToHackathon"
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useHackathonStore } from '~/stores/hackathonStore'
import Card from '~/components/ui/Card.vue'
import Table from '~/components/ui/Table.vue'

const store = useHackathonStore()
const router = useRouter()

// захардкожено для текущего пользователя
const hackathons = store.getHackathons

function goToHackathon(row: string[]) {
  const hackathon = store.hackathons.find(h => h.name === row[0])
  if (hackathon) router.push(`/hackathon/${hackathon.id}`)
}
</script>