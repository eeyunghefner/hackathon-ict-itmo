<template>
  <div>
    <Card>
      <h1>Хакатоны</h1>
    </Card>

    <Table
      :headers="['Название', 'Формат', 'Дата начала', 'Статус']"
      :rows="hackathons.map(h => [h.title, h.format, h.startDate, h.status])"
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

onMounted(() => {
  store.fetchHackathons({ status: "published", page: 1, limit: 10 }).catch((e) => console.error(e))
})

const hackathons = computed(() => store.getHackathons)

function goToHackathon(row: string[]) {
  const hackathon = store.hackathons.find(h => h.title === row[0])
  if (hackathon) router.push(`/hackathon/${hackathon.id}`)
}
</script>