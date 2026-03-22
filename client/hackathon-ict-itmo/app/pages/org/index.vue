<template>
  <div>
    <Card>
      <h1>Мои хакатоны</h1>

      <NuxtLink to="/org/hackathon/add">
        <Button variant="primary">Добавить хакатон</Button>
      </NuxtLink>
    </Card>

    <Card>
      <Table
        :headers="['Название', 'Формат', 'Дата начала', 'Статус']"
        :rows="hackathons.map(h => [h.title, h.format, h.startDate, h.status])"
        @row-click="goToHackathon"
      />
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useHackathonStore } from '~/stores/hackathonStore'
import Card from '~/components/ui/Card.vue'
import Table from '~/components/ui/Table.vue'
import Button from '~/components/ui/Button.vue'
import { NuxtLink } from '#components'

const store = useHackathonStore()
const router = useRouter()

onMounted(() => {
  store.fetchHackathons({ page: 1, limit: 10 }).catch((e) => console.error(e))
})

const hackathons = computed(() => store.getHackathons)

// Функция перехода по кликнутой строке таблицы
function goToHackathon(row: string[]) {
  const hackathon = store.hackathons.find(h => h.title === row[0])
  if (hackathon) router.push(`/org/hackathon/${hackathon.id}`)
}
</script>