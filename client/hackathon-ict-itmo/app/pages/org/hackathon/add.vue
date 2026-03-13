<template>
  <div>

    <h1>Создание хакатона</h1>

    <input v-model="hackathon.name" placeholder="Название" />
    <input v-model="hackathon.theme" placeholder="Тематика" />
    <input v-model="hackathon.format" placeholder="Формат" />

    <textarea v-model="hackathon.description" placeholder="Описание" />

    <input
      type="number"
      v-model="hackathon.participantLimit"
      placeholder="Лимит участников"
    />

    <input
      type="number"
      v-model="hackathon.teamLimit"
      placeholder="Лимит команд"
    />

    <textarea
      v-model="hackathon.regulations"
      placeholder="Регламент"
    />

    <button @click="create">Создать</button>

  </div>
</template>

<script setup lang="ts">
import OrgNavbar from "~/components/OrgNavbar.vue"
import { useHackathonStore } from "~/stores/hackathonStore"
import type { Hackathon } from "../../../../types/hackathon"

const store = useHackathonStore()
const router = useRouter()

const hackathon = ref<Hackathon>({
  id: Date.now().toString(),
  name: "",
  theme: "",
  format: "online",
  description: "",
  participantLimit: 0,
  teamLimit: 0,
  regulations: "",
  published: false,
  organizerId: "1"
})

function create() {
  store.addHackathon(hackathon.value)
  router.push(`/org/hackathon/${hackathon.value.id}`)
}
</script>