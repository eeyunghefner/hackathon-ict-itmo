<template>
  <div>
    <Card>
      <h1>{{ team?.name || "Загрузка..." }}</h1>

      <div v-if="team">
        <p>Капитан: {{ team.members.find(el => el.id === team?.captainId)?.name }}</p>

        <h3>Участники</h3>
        <ul>
          <li v-for="m in team.members" :key="m.id">
            {{ m.name }}
          </li>
        </ul>

        <Button @click="submitJoin" variant="primary" :disabled="submittingJoin" style="margin-right: 1rem;">
          Подать заявку в команду
        </Button>
        <Button @click="apply" variant="primary">
          Подать заявку на хакатон
        </Button>
      </div>
    </Card>

    <Card>
      <h2>Заявки на вступление</h2>

      <table>
        <thead>
          <tr>
            <th>Пользователь</th>
            <th>Статус</th>
            <th></th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in joinRequests" :key="r.id">
            <td>{{ r.userName || r.userId || "—" }}</td>
            <td>{{ r.status }}</td>
            <td>
              <button @click="approve(r.id)">Одобрить</button>
            </td>
            <td>
              <button @click="reject(r.id)">Отклонить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import Card from "~/components/ui/Card.vue"
import Button from "~/components/ui/Button.vue"
import { useTeamStore } from "~/stores/teamStore"

const route = useRoute()
const store = useTeamStore()

const teamId = computed(() => route.params.teamId as string)

const team = computed(() => store.getTeamById(teamId.value))
const joinRequests = computed(() => store.getJoinRequests(teamId.value))

const submittingJoin = ref(false)

onMounted(async () => {
  try {
    await store.fetchTeam(teamId.value)
    await store.fetchJoinRequests(teamId.value)
  } catch (e) {
    console.error(e)
    alert("Не удалось загрузить данные команды")
  }
})

const router = useRouter()

function apply() {
  router.push({ path: "/hackathons/apply", query: { teamId: teamId.value } })
}

async function submitJoin() {
  submittingJoin.value = true
  try {
    await store.submitJoinRequest(teamId.value)
    alert("Заявка отправлена")
  } catch (e) {
    console.error(e)
    alert("Не удалось отправить заявку")
  } finally {
    submittingJoin.value = false
  }
}

async function approve(requestId: string) {
  try {
    await store.approveJoinRequest(requestId, teamId.value)
    alert("Заявка одобрена")
  } catch (e) {
    console.error(e)
    alert("Не удалось одобрить заявку")
  }
}

async function reject(requestId: string) {
  try {
    await store.rejectJoinRequest(requestId, teamId.value)
    alert("Заявка отклонена")
  } catch (e) {
    console.error(e)
    alert("Не удалось отклонить заявку")
  }
}
</script>

