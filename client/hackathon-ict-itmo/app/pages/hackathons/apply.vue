<template>
  <Card>
    <h1>Подача заявки команды</h1>

    <p v-if="!teamId">Не найден `teamId` (ожидается в query).</p>

    <div v-else>
      <p>Команда: {{ teamId }}</p>

      <table>
        <thead>
          <tr>
            <th>Название</th>
            <th>Формат</th>
            <th>Дата начала</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="h in hackathons" :key="h.id">
            <td>{{ h.title }}</td>
            <td>{{ h.format }}</td>
            <td>{{ h.startDate }}</td>
            <td>
              <button @click="submitApplication(h.id)" :disabled="submitting">
                Подать заявку команды
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import Card from "~/components/ui/Card.vue"
import { useHackathonStore } from "~/stores/hackathonStore"
import type { HackathonListItem } from "../../../types/hackathon"

const route = useRoute()
const store = useHackathonStore()

const teamId = computed(() => {
  const v = route.query.teamId
  return typeof v === "string" && v.length ? v : ""
})

const hackathons = computed<HackathonListItem[]>(() => store.getHackathons)
const submitting = ref(false)

onMounted(async () => {
  try {
    await store.fetchHackathons({ status: "published", page: 1, limit: 10 })
  } catch (e) {
    console.error(e)
    alert("Не удалось загрузить хакатоны")
  }
})

async function submitApplication(hackathonId: string) {
  if (!teamId.value) return
  submitting.value = true
  try {
    await store.submitHackathonApplication(hackathonId, { teamId: teamId.value })
    alert("Заявка отправлена")
  } catch (e) {
    console.error(e)
    alert("Не удалось отправить заявку")
  } finally {
    submitting.value = false
  }
}
</script>

