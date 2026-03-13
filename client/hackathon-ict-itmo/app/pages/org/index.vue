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
        :headers="['Название', 'Тематика', 'Формат']"
        :rows="hackathons.map(h => [h.name, h.theme, h.format])"
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

// Получаем все хакатоны организатора с id "1" (захардкожено)
const hackathons = store.getOrganizerHackathons('1')

// Функция перехода по кликнутой строке таблицы
function goToHackathon(row: string[]) {
  const hackathon = store.hackathons.find(h => h.name === row[0])
  if (hackathon) router.push(`/org/hackathon/${hackathon.id}`)
}
</script>