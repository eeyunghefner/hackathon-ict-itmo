<template>
  <Card>
    <h1>Редактирование хакатона</h1>

    <div>
      <Button @tap="tab = 'info'" variant="secondary" class="right-margin">Общая информация</Button>
      <Button @tap="tab = 'participants'" variant="secondary" class="right-margin">Участники</Button>
      <Button @tap="tab = 'applications'" variant="secondary" class="right-margin">Заявки</Button>
    </div>

    <Card v-if="tab === 'info'">
      <FormField label="Название" v-model="hackathon.title" type="input" />
      <FormField label="Тематика" v-model="hackathon.theme" type="input" />
      <FormField label="Формат" v-model="hackathon.format" type="input" />
      <FormField label="Описание" v-model="hackathon.description" type="textarea" />
      <FormField label="Дата начала (YYYY-MM-DD)" v-model="hackathon.startDate" type="input" />
      <FormField label="Дата окончания (YYYY-MM-DD)" v-model="hackathon.endDate" type="input" />
      <FormField label="Лимит участников" v-model="hackathon.participantLimit" type="input" />
      <FormField label="Лимит команд" v-model="hackathon.teamLimit" type="input" />
      <FormField label="Правила" v-model="hackathon.rules" type="textarea" />

      <div>
        <Button @click="save" variant="primary" class="right-margin">Сохранить</Button>
        <Button @click="togglePublish" variant="primary" class="right-margin">
          {{ hackathon.status === 'published' ? 'Снять с публикации' : 'Опубликовать' }}
        </Button>
        <Button @click="archive" variant="secondary">Архивировать</Button>
      </div>

      <h3>Расписание</h3>
      <Table
        :headers="['Событие', 'Время', 'Действие']"
        :rows="events.map(e => [e.name, e.time, 'Удалить'])"
      />
    </Card>

    <Card v-if="tab === 'participants'">
      <Table
        :headers="['Команда', 'Участники']"
        :rows="registrations.map(r => [r.teamName, r.members.map(m => m.name).join(', ')])"
      />
    </Card>

    <Card v-if="tab === 'applications'">
      <Table
        :headers="['Команда', 'Участники']"
        :rows="applications.map(a => [a.teamName, a.members.map(m => m.name).join(', ')])"
      />
    </Card>
  </Card>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { useHackathonStore } from '~/stores/hackathonStore'
import Card from '~/components/ui/Card.vue'
import Table from '~/components/ui/Table.vue'
import FormField from '~/components/ui/FormField.vue'
import Button from '~/components/ui/Button.vue'
import type { HackathonDetail } from '../../../../types/hackathon'

const route = useRoute()
const store = useHackathonStore()
const id = route.params.hackathon_id as string

const hackathon = reactive<HackathonDetail>({
  id,
  title: "",
  theme: "",
  description: "",
  format: "online",
  startDate: "",
  endDate: "",
  participantLimit: 0,
  teamLimit: 0,
  rules: "",
  status: "draft"
})
const events = store.getSchedule(id)
const registrations = store.getRegistrations(id)
const applications = store.getApplications(id)

const tab = ref('info')

onMounted(async () => {
  try {
    const data = await store.fetchHackathon(id)
    Object.assign(hackathon, data)
  } catch (error) {
    console.error(error)
    alert("Не удалось загрузить хакатон")
  }
})

async function save() {
  try {
    const data = await store.updateHackathon(id, {
      title: hackathon.title,
      theme: hackathon.theme,
      description: hackathon.description,
      format: hackathon.format,
      startDate: hackathon.startDate,
      endDate: hackathon.endDate,
      participantLimit: hackathon.participantLimit,
      teamLimit: hackathon.teamLimit,
      rules: hackathon.rules
    })
    Object.assign(hackathon, data)
    alert("Сохранено!")
  } catch (error) {
    console.error(error)
    alert("Не удалось сохранить хакатон")
  }
}

async function togglePublish() {
  try {
    const data = hackathon.status === "published"
      ? await store.unpublishHackathon(id)
      : await store.publishHackathon(id)
    Object.assign(hackathon, data)
  } catch (error) {
    console.error(error)
    alert("Не удалось изменить статус публикации")
  }
}

async function archive() {
  try {
    const data = await store.archiveHackathon(id)
    Object.assign(hackathon, data)
  } catch (error) {
    console.error(error)
    alert("Не удалось архивировать")
  }
}
</script>

<style>
.right-margin {
    margin-right: 1.5rem;
}
</style>