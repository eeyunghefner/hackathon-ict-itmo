<template>
  <Card>
    <h1>Редактирование хакатона</h1>

    <div>
      <Button @click="tab = 'info'" variant="secondary" class="right-margin">Общая информация</Button>
      <Button @click="tab = 'participants'" variant="secondary" class="right-margin">Участники</Button>
      <Button @click="tab = 'applications'" variant="secondary" class="right-margin">Заявки</Button>
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
      <div class="events-manager">
        <form class="event-form" @submit.prevent="submitEvent">
          <h4>{{ editingEventId ? 'Редактирование события' : 'Добавить событие' }}</h4>

          <label>Название</label>
          <input v-model="eventForm.title" type="text" />

          <label>Описание</label>
          <textarea v-model="eventForm.description" rows="3" />

          <label>Начало</label>
          <input v-model="eventForm.startTime" type="datetime-local" />

          <label>Конец</label>
          <input v-model="eventForm.endTime" type="datetime-local" />

          <label>Room ID</label>
          <input v-model="eventForm.roomId" type="text" />

          <div class="event-form-actions">
            <Button variant="primary" :disabled="submittingEvent" @click="submitEvent">
              {{ editingEventId ? 'Сохранить' : 'Добавить' }}
            </Button>
            <Button
              v-if="editingEventId"
              variant="secondary"
              :disabled="submittingEvent"
              @click="cancelEdit"
            >
              Отмена
            </Button>
          </div>
        </form>

        <table class="events-table">
          <thead>
            <tr>
              <th>Событие</th>
              <th>Время</th>
              <th>Room ID</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in events" :key="e.id">
              <td>{{ e.title ?? e.name ?? "—" }}</td>
              <td>{{ formatEventTime(e) }}</td>
              <td>{{ e.roomId ?? "—" }}</td>
              <td class="events-actions">
                <Button
                  variant="secondary"
                  @click="startEdit(e)"
                  :disabled="submittingEvent || deletingEventId === e.id"
                >
                  Редактировать
                </Button>
                <Button
                  variant="primary"
                  style="margin-left: 0.5rem;"
                  @click="removeEvent(e)"
                  :disabled="deletingEventId === e.id"
                >
                  Удалить
                </Button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </Card>

    <Card v-if="tab === 'participants'">
      <Table
        :headers="['Команда', 'Участники']"
        :rows="registrations.map(r => [r.teamName, r.members.map(m => m.name).join(', ')])"
      />
    </Card>

    <Card v-if="tab === 'applications'">
      <table>
        <thead>
          <tr>
            <th>Команда</th>
            <th>Статус</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="a in hackathonApplications" :key="a.id">
            <td>{{ a.teamName }}</td>
            <td>{{ a.status }}</td>
            <td>
              <button @click="approve(a.id)">Одобрить</button>
            </td>
            <td>
              <button @click="reject(a.id)">Отклонить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </Card>
  </Card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { useHackathonStore } from '~/stores/hackathonStore'
import Card from '~/components/ui/Card.vue'
import FormField from '~/components/ui/FormField.vue'
import Button from '~/components/ui/Button.vue'
import Table from '~/components/ui/Table.vue'
import type { HackathonDetail, HackathonEvent, CreateHackathonEventRequest } from '../../../../types/hackathon'

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
const events = computed(() => store.getSchedule(id))
const registrations = store.getRegistrations(id)
const hackathonApplications = computed(() => store.getHackathonApplications(id))

const tab = ref('info')

onMounted(async () => {
  try {
    const data = await store.fetchHackathon(id)
    Object.assign(hackathon, data)
    await store.fetchHackathonApplications(id)
    await store.fetchEvents(id)
  } catch (error) {
    console.error(error)
    alert("Не удалось загрузить хакатон")
  }
})

const editingEventId = ref<string | null>(null)
const submittingEvent = ref(false)
const deletingEventId = ref<string | null>(null)

const eventForm = reactive<{
  title: string
  description: string
  startTime: string
  endTime: string
  roomId: string
}>({
  title: "",
  description: "",
  startTime: "",
  endTime: "",
  roomId: ""
})

function normalizeDatetimeLocal(value?: string) {
  if (!value) return ""
  // Accept formats like `2026-05-10T10:00` or `2026-05-10T10:00:00`
  return value.length >= 16 ? value.slice(0, 16) : value
}

function formatEventTime(e: HackathonEvent) {
  const start = e.startTime ?? e.time
  const end = e.endTime
  if (start && end) return `${start} - ${end}`
  return start ?? ""
}

function resetEventForm() {
  eventForm.title = ""
  eventForm.description = ""
  eventForm.startTime = ""
  eventForm.endTime = ""
  eventForm.roomId = ""
}

function cancelEdit() {
  editingEventId.value = null
  resetEventForm()
}

function startEdit(e: HackathonEvent) {
  editingEventId.value = e.id
  eventForm.title = e.title ?? e.name ?? ""
  eventForm.description = e.description ?? ""
  eventForm.startTime = normalizeDatetimeLocal(e.startTime)
  eventForm.endTime = normalizeDatetimeLocal(e.endTime)
  eventForm.roomId = e.roomId ?? ""
}

async function submitEvent() {
  if (submittingEvent.value) return
  if (!eventForm.title.trim()) {
    alert("Укажите название события")
    return
  }
  if (!eventForm.startTime || !eventForm.endTime) {
    alert("Укажите время начала и окончания")
    return
  }
  if (!eventForm.roomId.trim()) {
    alert("Укажите roomId")
    return
  }

  submittingEvent.value = true
  try {
    const payload: CreateHackathonEventRequest = {
      title: eventForm.title,
      description: eventForm.description,
      startTime: eventForm.startTime,
      endTime: eventForm.endTime,
      roomId: eventForm.roomId
    }

    if (editingEventId.value) {
      await store.updateEvent(editingEventId.value, id, payload)
      alert("Событие обновлено")
    } else {
      await store.createEvent(id, payload)
      alert("Событие добавлено")
    }

    cancelEdit()
  } catch (e) {
    console.error(e)
    alert("Не удалось сохранить событие")
  } finally {
    submittingEvent.value = false
  }
}

async function removeEvent(e: HackathonEvent) {
  if (deletingEventId.value) return
  const ok = window.confirm("Удалить событие?")
  if (!ok) return

  deletingEventId.value = e.id
  try {
    await store.deleteEvent(e.id, id)
    alert("Событие удалено")

    // Если удалили активное редактируемое событие, сбросим форму.
    if (editingEventId.value === e.id) cancelEdit()
  } catch (err) {
    console.error(err)
    alert("Не удалось удалить событие")
  } finally {
    deletingEventId.value = null
  }
}

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

async function approve(applicationId: string) {
  try {
    await store.approveHackathonApplication(applicationId, id)
    alert("Заявка одобрена")
  } catch (error) {
    console.error(error)
    alert("Не удалось одобрить заявку")
  }
}

async function reject(applicationId: string) {
  try {
    await store.rejectHackathonApplication(applicationId, id)
    alert("Заявка отклонена")
  } catch (error) {
    console.error(error)
    alert("Не удалось отклонить заявку")
  }
}
</script>

<style>
.right-margin {
    margin-right: 1.5rem;
}

.events-manager {
  margin-top: 1rem;
}

.event-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 600px;
}

.event-form input,
.event-form textarea {
  padding: 0.5rem;
}

.event-form-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.events-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.events-table th,
.events-table td {
  padding: 0.5rem;
  border-bottom: 1px solid #eaeaea;
  vertical-align: top;
}

.events-actions {
  white-space: nowrap;
}
</style>