<template>
  <Card>
    <h1>Редактирование хакатона</h1>

    <div>
      <Button @click="tab = 'info'" variant="secondary" class="right-margin">Общая информация</Button>
      <Button @click="tab = 'participants'" variant="secondary" class="right-margin">Участники</Button>
      <Button @click="tab = 'applications'" variant="secondary" class="right-margin">Заявки</Button>
    </div>

    <Card v-if="tab === 'info'">
      <FormField label="Название" v-model="hackathon.name" type="input" />
      <FormField label="Тематика" v-model="hackathon.theme" type="input" />
      <FormField label="Формат" v-model="hackathon.format" type="input" />
      <FormField label="Описание" v-model="hackathon.description" type="textarea" />
      <FormField label="Лимит участников" v-model="hackathon.participantLimit" type="input" />
      <FormField label="Лимит команд" v-model="hackathon.teamLimit" type="input" />
      <FormField label="Регламент" v-model="hackathon.regulations" type="textarea" />

      <Button @click="toggle" variant="primary">
        {{ hackathon.published ? 'Снять с публикации' : 'Опубликовать' }}
      </Button>

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

const route = useRoute()
const store = useHackathonStore()
const id = route.params.hackathon_id as string

const hackathon = reactive({ ...store.getHackathonById(id)! })
const events = store.getSchedule(id)
const registrations = store.getRegistrations(id)
const applications = store.getApplications(id)

const tab = ref('info')

function toggle() {
  store.togglePublication(id)
}
</script>

<style>
.right-margin {
    margin-right: 1.5rem;
}
</style>