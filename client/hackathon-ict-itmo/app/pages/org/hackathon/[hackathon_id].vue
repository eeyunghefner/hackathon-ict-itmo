<template>
  <div>
    <h1>Редактирование хакатона</h1>

    <div>

      <button @click="tab = 'info'">Общая информация</button>
      <button @click="tab = 'participants'">Участники</button>
      <button @click="tab = 'applications'">Заявки</button>

    </div>

    <div v-if="tab === 'info'">

      <input v-model="hackathon.name" />
      <input v-model="hackathon.theme" />
      <input v-model="hackathon.format" />

      <textarea v-model="hackathon.description"></textarea>

      <input type="number" v-model="hackathon.participantLimit" />
      <input type="number" v-model="hackathon.teamLimit" />

      <textarea v-model="hackathon.regulations"></textarea>

      <button @click="toggle">
        {{ hackathon.published ? "Снять с публикации" : "Опубликовать" }}
      </button>

      <h3>Расписание</h3>

      <table>
        <tr v-for="event in events" :key="event.id">
          <td>{{ event.name }}</td>
          <td>{{ event.time }}</td>
          <td>
            <button @click="removeEvent(event.id)">Удалить</button>
          </td>
        </tr>
      </table>

      <input v-model="newEvent.name" placeholder="Название события" />
      <input v-model="newEvent.time" placeholder="Время" />

      <button @click="addEvent">Добавить событие</button>

    </div>

    <div v-if="tab === 'participants'">

      <table>

        <tr v-for="team in registrations" :key="team.id">
          <td>{{ team.teamName }}</td>

          <td>
            <div v-for="member in team.members" :key="member.id">
              {{ member.name }}
            </div>
          </td>

        </tr>

      </table>

    </div>

    <div v-if="tab === 'applications'">

      <table>

        <tr v-for="team in applications" :key="team.id">

          <td>{{ team.teamName }}</td>

          <td>
            <div v-for="member in team.members" :key="member.id">
              {{ member.name }}
            </div>
          </td>

        </tr>

      </table>

    </div>

  </div>
</template>

<script setup lang="ts">

import OrgNavbar from "~/components/OrgNavbar.vue"
import { useHackathonStore } from "~/stores/hackathonStore"

const route = useRoute()

const store = useHackathonStore()

const id = route.params.hackathon_id as string

const hackathon = reactive({ ...store.getHackathonById(id)! })

const events = store.getSchedule(id)

const registrations = store.getRegistrations(id)

const applications = store.getApplications(id)

const tab = ref("info")

const newEvent = ref({
  name: "",
  time: ""
})

function toggle() {
  store.togglePublication(id)
}

function addEvent() {

  store.addEvent(id, {
    id: Date.now().toString(),
    name: newEvent.value.name,
    time: newEvent.value.time
  })

}

function removeEvent(eventId: string) {
  store.removeEvent(id, eventId)
}

</script>