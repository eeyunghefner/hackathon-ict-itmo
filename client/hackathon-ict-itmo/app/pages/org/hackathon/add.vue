<template>
  <Card>
    <h1>Создание хакатона</h1>

    <FormField label="Название" v-model="hackathon.name" type="input" />
    <FormField label="Тематика" v-model="hackathon.theme" type="input" />
    <FormField label="Формат" v-model="hackathon.format" type="input" />
    <FormField label="Описание" v-model="hackathon.description" type="textarea" />
    <FormField label="Лимит участников" v-model="hackathon.participantLimit" type="input" />
    <FormField label="Лимит команд" v-model="hackathon.teamLimit" type="input" />
    <FormField label="Регламент" v-model="hackathon.regulations" type="textarea" />

    <Button @tap="create" variant="primary">Создать</Button>
  </Card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useHackathonStore } from '~/stores/hackathonStore'
import Card from '~/components/ui/Card.vue'
import FormField from '~/components/ui/FormField.vue'
import Button from '~/components/ui/Button.vue'
import type { Hackathon } from '../../../../types/hackathon'

const store = useHackathonStore()
const router = useRouter()

const hackathon = ref<Hackathon>({
  id: Date.now().toString(),
  name: '',
  theme: '',
  format: 'online',
  description: '',
  participantLimit: 0,
  teamLimit: 0,
  regulations: '',
  published: false,
  organizerId: '1'
})

function create() {
  store.addHackathon(hackathon.value)
  router.push(`/org/hackathon/${hackathon.value.id}`)
}
</script>